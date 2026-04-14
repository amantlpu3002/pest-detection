"""
utils.py
--------
Helper utilities for the Streamlit app.
"""

import os
import sys
import torch
from PIL import Image

# Allow import from sibling src/ directory
SRC_DIR = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, os.path.abspath(SRC_DIR))

from model import load_model
from predict import predict_image

# ─────────────────────────────────────────────────────────────────────────────
# Device
# ─────────────────────────────────────────────────────────────────────────────
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# ─────────────────────────────────────────────────────────────────────────────
# Model loader (cached by Streamlit)
# ─────────────────────────────────────────────────────────────────────────────

def load_classes(data_dir: str):
    """Read class names from classes.txt in the IP102 dataset directory."""
    classes_file = os.path.join(data_dir, 'classes.txt')
    with open(classes_file, 'r') as f:
        return [line.strip() for line in f.readlines()]


def load_trained_model(checkpoint_path: str, num_classes: int = 102):
    """Load the trained model; returns None if checkpoint not found."""
    if not os.path.exists(checkpoint_path):
        return None
    return load_model(checkpoint_path, num_classes=num_classes, device=str(DEVICE))


def run_inference(pil_image: Image.Image, model, classes, top_k: int = 5):
    """
    Run pest classification on a PIL image.

    Returns list of top-k dicts:
      [{'rank', 'class_id', 'class_name', 'confidence'}, ...]
    """
    return predict_image(pil_image, model, classes, DEVICE, top_k=top_k)


# ─────────────────────────────────────────────────────────────────────────────
# Severity colour mapping (for UI badges)
# ─────────────────────────────────────────────────────────────────────────────
SEVERITY_COLORS = {
    'High':    '#e74c3c',
    'Medium':  '#f39c12',
    'Low':     '#2ecc71',
    'Unknown': '#95a5a6',
}

SEVERITY_EMOJIS = {
    'High':    '🔴',
    'Medium':  '🟡',
    'Low':     '🟢',
    'Unknown': '⚪',
}

CROP_EMOJIS = {
    'Rice':        '🌾',
    'Corn':        '🌽',
    'Wheat':       '🌾',
    'Cotton':      '🌿',
    'Soybean':     '🫘',
    'Potato':      '🥔',
    'Tomato':      '🍅',
    'Apple':       '🍎',
    'Grape':       '🍇',
    'Peach':       '🍑',
    'Cherry':      '🍒',
    'Cabbage':     '🥬',
    'Onion':       '🧅',
    'General':     '🌱',
}


def crop_emoji(crop_str: str) -> str:
    for key, emoji in CROP_EMOJIS.items():
        if key.lower() in crop_str.lower():
            return emoji
    return '🌱'
