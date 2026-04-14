"""
dataset.py
----------
Dataset class and DataLoaders for the IP102 insect pest dataset.
Handles data loading, augmentation, and class imbalance.
"""

import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from collections import Counter


class IP102Dataset(Dataset):
    """
    PyTorch Dataset for IP102 Insect Pest Classification.

    Dataset folder structure expected:
        root_dir/
            classification/
                train/  val/  test/   (each with 102 class folders)
            classes.txt
            train.txt  val.txt  test.txt
    """

    def __init__(self, root_dir, split='train', transform=None):
        """
        Args:
            root_dir (str): Path to IP102 dataset root directory.
            split    (str): One of 'train', 'val', 'test'.
            transform     : torchvision transforms to apply.
        """
        self.root_dir = root_dir
        self.split = split
        self.transform = transform

        # ── Load class names ────────────────────────────────────────────────
        classes_file = os.path.join(root_dir, 'classes.txt')
        with open(classes_file, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]
        self.num_classes = len(self.classes)   # 102

        # ── Load image paths + labels from split txt file ───────────────────
        txt_file = os.path.join(root_dir, f'{split}.txt')
        self.samples = []
        with open(txt_file, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                img_path = os.path.join(root_dir, parts[0])
                label = int(parts[1])
                self.samples.append((img_path, label))

        print(f"[{split.upper()}] Loaded {len(self.samples)} images "
              f"across {self.num_classes} classes.")

    # ────────────────────────────────────────────────────────────────────────
    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        try:
            image = Image.open(img_path).convert('RGB')
        except Exception as e:
            print(f"Warning: Could not load image {img_path}: {e}")
            image = Image.new('RGB', (224, 224), color=(0, 0, 0))

        if self.transform:
            image = self.transform(image)

        return image, label

    # ────────────────────────────────────────────────────────────────────────
    def get_class_weights(self):
        """
        Compute inverse-frequency class weights to handle the class imbalance
        present in IP102. Passed to nn.CrossEntropyLoss(weight=...).
        """
        labels = [s[1] for s in self.samples]
        counter = Counter(labels)
        total = len(labels)
        weights = [
            total / (self.num_classes * max(counter[i], 1))
            for i in range(self.num_classes)
        ]
        return torch.FloatTensor(weights)

    def get_class_distribution(self):
        """Return dict mapping class_name → sample count."""
        labels = [s[1] for s in self.samples]
        counter = Counter(labels)
        return {self.classes[k]: v for k, v in sorted(counter.items())}


# ────────────────────────────────────────────────────────────────────────────
# Transforms
# ────────────────────────────────────────────────────────────────────────────

def get_transforms(split='train', img_size=224):
    """
    Returns appropriate torchvision transforms for each split.

    Training  : heavy augmentation to improve generalisation.
    Val / Test: only resize + normalise.
    """
    imagenet_mean = [0.485, 0.456, 0.406]
    imagenet_std  = [0.229, 0.224, 0.225]

    if split == 'train':
        return transforms.Compose([
            transforms.Resize((img_size + 32, img_size + 32)),
            transforms.RandomCrop(img_size),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomVerticalFlip(p=0.2),
            transforms.ColorJitter(
                brightness=0.3, contrast=0.3,
                saturation=0.3, hue=0.1
            ),
            transforms.RandomRotation(degrees=20),
            transforms.RandomGrayscale(p=0.05),
            transforms.ToTensor(),
            transforms.Normalize(mean=imagenet_mean, std=imagenet_std),
            transforms.RandomErasing(p=0.1),          # Cutout-style regularisation
        ])
    else:
        return transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=imagenet_mean, std=imagenet_std),
        ])


# ────────────────────────────────────────────────────────────────────────────
# DataLoader factory
# ────────────────────────────────────────────────────────────────────────────

def get_dataloaders(root_dir, batch_size=32, img_size=224, num_workers=4):
    """
    Build DataLoaders for train, val, and test splits.

    Returns:
        loaders  (dict): {'train': DataLoader, 'val': DataLoader, 'test': DataLoader}
        datasets (dict): {'train': Dataset,    'val': Dataset,    'test': Dataset}
    """
    datasets = {}
    loaders  = {}

    for split in ['train', 'val', 'test']:
        transform = get_transforms(split, img_size)
        datasets[split] = IP102Dataset(root_dir, split, transform)
        loaders[split]  = DataLoader(
            datasets[split],
            batch_size=batch_size,
            shuffle=(split == 'train'),
            num_workers=num_workers,
            pin_memory=True,
            drop_last=(split == 'train'),
        )

    return loaders, datasets
