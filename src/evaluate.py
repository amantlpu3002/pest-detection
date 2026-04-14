"""
evaluate.py
-----------
Post-training evaluation for the IP102 Pest Classifier.

Outputs:
  - Top-1 and Top-5 accuracy on the test set
  - Full classification report (precision, recall, F1 per class)
  - Confusion matrix heatmap  → models/confusion_matrix.png
  - Training curves plot      → models/training_curves.png
"""

import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import torch
from tqdm import tqdm
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    top_k_accuracy_score,
)

sys.path.insert(0, os.path.dirname(__file__))
from dataset import get_dataloaders
from model import load_model


# ─────────────────────────────────────────────────────────────────────────────

@torch.no_grad()
def evaluate_model(model, loader, device, class_names):
    model.eval()
    all_preds, all_labels, all_probs = [], [], []

    for images, labels in tqdm(loader, desc='Evaluating'):
        images = images.to(device)
        outputs = model(images)
        probs   = torch.softmax(outputs, dim=1)
        _, preds = outputs.max(1)

        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.numpy())
        all_probs.extend(probs.cpu().numpy())

    all_preds  = np.array(all_preds)
    all_labels = np.array(all_labels)
    all_probs  = np.array(all_probs)

    # ── Metrics ──────────────────────────────────────────────────────────────
    top1_acc = (all_preds == all_labels).mean() * 100
    top5_acc = top_k_accuracy_score(all_labels, all_probs, k=5) * 100

    print(f"\n{'='*55}")
    print(f"  Test Results")
    print(f"{'='*55}")
    print(f"  Top-1 Accuracy : {top1_acc:.2f}%")
    print(f"  Top-5 Accuracy : {top5_acc:.2f}%")
    print(f"{'='*55}\n")

    print("Per-Class Classification Report:")
    print(classification_report(
        all_labels, all_preds,
        target_names=class_names,
        digits=3,
        zero_division=0,
    ))

    return all_preds, all_labels, all_probs


# ─────────────────────────────────────────────────────────────────────────────

def plot_training_curves(history_path: str, save_dir: str):
    with open(history_path) as f:
        h = json.load(f)

    epochs = range(1, len(h['train_loss']) + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Training History — IP102 Pest Classifier', fontsize=14)

    # Loss
    ax1.plot(epochs, h['train_loss'], 'b-o', label='Train Loss', markersize=4)
    ax1.plot(epochs, h['val_loss'],   'r-o', label='Val Loss',   markersize=4)
    ax1.set_title('Loss Curve')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(alpha=0.3)

    # Accuracy
    ax2.plot(epochs, h['train_acc'], 'b-o', label='Train Acc', markersize=4)
    ax2.plot(epochs, h['val_acc'],   'r-o', label='Val Acc',   markersize=4)
    ax2.set_title('Accuracy Curve')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    out = os.path.join(save_dir, 'training_curves.png')
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Training curves saved → {out}")


def plot_confusion_matrix(all_preds, all_labels, class_names, save_dir,
                          top_n=20):
    """
    Plot confusion matrix for top-N most confused classes to keep it readable.
    """
    cm      = confusion_matrix(all_labels, all_preds)
    # Select top_n classes with most errors
    errors  = cm.sum(axis=1) - np.diag(cm)
    top_idx = np.argsort(errors)[-top_n:]
    cm_sub  = cm[np.ix_(top_idx, top_idx)]
    names   = [class_names[i] for i in top_idx]

    plt.figure(figsize=(16, 14))
    sns.heatmap(
        cm_sub, annot=True, fmt='d', cmap='Blues',
        xticklabels=names, yticklabels=names,
        linewidths=0.5,
    )
    plt.title(f'Confusion Matrix — Top {top_n} Most Confused Classes')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()

    out = os.path.join(save_dir, 'confusion_matrix.png')
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Confusion matrix saved → {out}")


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    DATA_DIR  = '../data/ip102'
    MODEL_DIR = '../models'

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")

    # Load model
    model = load_model(
        os.path.join(MODEL_DIR, 'best_model.pth'),
        num_classes=102,
        device=str(device),
    )

    # Load data
    loaders, datasets = get_dataloaders(
        root_dir=DATA_DIR, batch_size=64, num_workers=4)
    class_names = datasets['test'].classes

    # Evaluate
    preds, labels, probs = evaluate_model(
        model, loaders['test'], device, class_names)

    # Plots
    plot_training_curves(
        os.path.join(MODEL_DIR, 'history.json'), MODEL_DIR)
    plot_confusion_matrix(preds, labels, class_names, MODEL_DIR, top_n=20)
