"""
model.py
--------
EfficientNet-B3 based pest classifier using timm (PyTorch Image Models).
Pretrained on ImageNet, fine-tuned on IP102 (102 classes).
"""

import torch
import torch.nn as nn
import timm


class PestClassifier(nn.Module):
    """
    EfficientNet-B3 backbone + custom classification head.

    Architecture:
        EfficientNet-B3 (pretrained, frozen early layers)
            ↓  Global Average Pool  →  1536-dim feature vector
        Dropout(0.3)
        Linear(1536 → 512)  +  BatchNorm  +  ReLU
        Dropout(0.15)
        Linear(512 → 102)
    """

    def __init__(
        self,
        num_classes: int = 102,
        model_name: str = 'efficientnet_b3',
        pretrained: bool = True,
        dropout: float = 0.3,
    ):
        super().__init__()

        # ── Backbone ────────────────────────────────────────────────────────
        self.backbone = timm.create_model(
            model_name,
            pretrained=pretrained,
            num_classes=0,        # Strip original classifier
            global_pool='avg',    # Global Average Pooling
        )
        in_features = self.backbone.num_features   # 1536 for B3

        # ── Custom head ─────────────────────────────────────────────────────
        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout / 2),
            nn.Linear(512, num_classes),
        )

        # Weight initialisation for custom head
        self._init_weights()

    # ────────────────────────────────────────────────────────────────────────
    def _init_weights(self):
        for m in self.classifier.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode='fan_out')
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, nn.BatchNorm1d):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.backbone(x)      # (B, 1536)
        logits   = self.classifier(features)   # (B, 102)
        return logits

    def freeze_backbone(self):
        """Freeze backbone layers — useful for initial warm-up epochs."""
        for param in self.backbone.parameters():
            param.requires_grad = False

    def unfreeze_backbone(self):
        """Unfreeze backbone for full fine-tuning."""
        for param in self.backbone.parameters():
            param.requires_grad = True

    def count_parameters(self):
        total     = sum(p.numel() for p in self.parameters())
        trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        return total, trainable


# ────────────────────────────────────────────────────────────────────────────
# Factory helpers
# ────────────────────────────────────────────────────────────────────────────

def get_model(
    num_classes: int = 102,
    model_name: str = 'efficientnet_b3',
    pretrained: bool = True,
) -> PestClassifier:
    """Instantiate and return the PestClassifier."""
    model = PestClassifier(
        num_classes=num_classes,
        model_name=model_name,
        pretrained=pretrained,
    )
    total, trainable = model.count_parameters()
    print(f"Model: {model_name}  |  "
          f"Total params: {total/1e6:.2f}M  |  "
          f"Trainable: {trainable/1e6:.2f}M")
    return model


def save_model(model, optimizer, epoch, val_acc, path):
    """Save full checkpoint."""
    torch.save({
        'epoch':                epoch,
        'model_state_dict':     model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'val_acc':              val_acc,
    }, path)
    print(f"  ✅ Checkpoint saved → {path}  (val_acc={val_acc:.2f}%)")


def load_model(checkpoint_path: str, num_classes: int = 102,
               device: str = 'cpu') -> PestClassifier:
    """Load model from checkpoint for inference."""
    model = get_model(num_classes=num_classes, pretrained=False)
    ckpt  = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(ckpt['model_state_dict'])
    model.to(device)
    model.eval()
    print(f"Model loaded from {checkpoint_path}  "
          f"(epoch={ckpt.get('epoch','?')}, "
          f"val_acc={ckpt.get('val_acc', '?'):.2f}%)")
    return model
