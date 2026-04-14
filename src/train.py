"""
train.py
--------
Complete training pipeline for the IP102 Pest Classifier.

Features:
  - EfficientNet-B3 with ImageNet pretrained weights
  - Two-phase training: warm-up (frozen backbone) → full fine-tuning
  - Weighted CrossEntropyLoss to handle IP102 class imbalance
  - AdamW + CosineAnnealingLR scheduler
  - Automatic mixed precision (AMP) for faster GPU training
  - Best model checkpointing + training history saved as JSON
"""

import os
import sys
import json
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.cuda.amp import GradScaler, autocast
from torch.optim.lr_scheduler import CosineAnnealingLR
from tqdm import tqdm

# Allow running from src/ directly
sys.path.insert(0, os.path.dirname(__file__))
from dataset import get_dataloaders
from model import get_model, save_model


# ─────────────────────────────────────────────────────────────────────────────
# One epoch helpers
# ─────────────────────────────────────────────────────────────────────────────

def train_one_epoch(model, loader, criterion, optimizer, scaler, device):
    model.train()
    running_loss, correct, total = 0.0, 0, 0

    pbar = tqdm(loader, desc='  Train', leave=False)
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad(set_to_none=True)

        with autocast():                        # Mixed precision forward pass
            outputs = model(images)
            loss    = criterion(outputs, labels)

        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        scaler.step(optimizer)
        scaler.update()

        running_loss += loss.item() * images.size(0)
        _, predicted  = outputs.max(1)
        total        += labels.size(0)
        correct      += predicted.eq(labels).sum().item()

        pbar.set_postfix(
            loss=f'{running_loss/total:.4f}',
            acc=f'{100.*correct/total:.1f}%'
        )

    return running_loss / total, 100. * correct / total


@torch.no_grad()
def validate(model, loader, criterion, device):
    model.eval()
    running_loss, correct, total = 0.0, 0, 0

    pbar = tqdm(loader, desc='  Val  ', leave=False)
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)

        with autocast():
            outputs = model(images)
            loss    = criterion(outputs, labels)

        running_loss += loss.item() * images.size(0)
        _, predicted  = outputs.max(1)
        total        += labels.size(0)
        correct      += predicted.eq(labels).sum().item()

        pbar.set_postfix(
            loss=f'{running_loss/total:.4f}',
            acc=f'{100.*correct/total:.1f}%'
        )

    return running_loss / total, 100. * correct / total


# ─────────────────────────────────────────────────────────────────────────────
# Main training function
# ─────────────────────────────────────────────────────────────────────────────

def train(config: dict):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\n{'='*60}")
    print(f"  Pest Detection Training  |  Device: {device}")
    print(f"{'='*60}\n")

    os.makedirs(config['save_dir'], exist_ok=True)

    # ── Data ─────────────────────────────────────────────────────────────────
    loaders, datasets = get_dataloaders(
        root_dir=config['data_dir'],
        batch_size=config['batch_size'],
        img_size=config['img_size'],
        num_workers=config['num_workers'],
    )

    # ── Model ────────────────────────────────────────────────────────────────
    model = get_model(num_classes=102, model_name=config['model_name'])
    model = model.to(device)

    # ── Loss (weighted for class imbalance) ───────────────────────────────
    class_weights = datasets['train'].get_class_weights().to(device)
    criterion     = nn.CrossEntropyLoss(weight=class_weights, label_smoothing=0.1)

    # ── Optimiser — different LR for backbone vs head ─────────────────────
    optimizer = optim.AdamW([
        {'params': model.backbone.parameters(),   'lr': config['lr'] * 0.1},
        {'params': model.classifier.parameters(), 'lr': config['lr']},
    ], weight_decay=1e-4)

    scheduler = CosineAnnealingLR(
        optimizer,
        T_max=config['epochs'],
        eta_min=1e-6,
    )

    scaler = GradScaler()   # For automatic mixed precision

    # ── Training loop ────────────────────────────────────────────────────────
    best_val_acc = 0.0
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

    for epoch in range(1, config['epochs'] + 1):
        start = time.time()
        print(f"\nEpoch [{epoch:02d}/{config['epochs']:02d}]")

        # Phase 1: warm-up with frozen backbone for first few epochs
        if epoch <= config.get('warmup_epochs', 3):
            model.freeze_backbone()
        else:
            model.unfreeze_backbone()

        train_loss, train_acc = train_one_epoch(
            model, loaders['train'], criterion, optimizer, scaler, device)

        val_loss, val_acc = validate(
            model, loaders['val'], criterion, device)

        scheduler.step()
        elapsed = time.time() - start

        # Log
        print(f"  Train → Loss: {train_loss:.4f}  Acc: {train_acc:.2f}%")
        print(f"  Val   → Loss: {val_loss:.4f}  Acc: {val_acc:.2f}%  "
              f"[{elapsed:.0f}s]")

        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)

        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            save_model(
                model, optimizer, epoch, val_acc,
                os.path.join(config['save_dir'], 'best_model.pth')
            )

        # Save history after every epoch
        with open(os.path.join(config['save_dir'], 'history.json'), 'w') as f:
            json.dump(history, f, indent=2)

    print(f"\n{'='*60}")
    print(f"  Training complete!  Best Val Acc: {best_val_acc:.2f}%")
    print(f"  Model saved → {config['save_dir']}/best_model.pth")
    print(f"{'='*60}\n")
    return history


# ─────────────────────────────────────────────────────────────────────────────
# Entry point — edit config as needed
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':

    config = {
        # ── Paths ──────────────────────────────────────────────────────────
        'data_dir':  'data/IP102',    # Root folder of IP102 dataset
        'save_dir':  'models',        # Where checkpoints are saved

        # ── Model ──────────────────────────────────────────────────────────
        'model_name': 'efficientnet_b3', # timm model name

        # ── Training ───────────────────────────────────────────────────────
        'img_size':      224,
        'batch_size':    32,
        'epochs':        30,
        'warmup_epochs': 3,              # Epochs with frozen backbone
        'lr':            1e-3,
        'num_workers':   4,
    }

    train(config)
