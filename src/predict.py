"""
predict.py
----------
Single-image inference utilities used by the Streamlit app.
"""

import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from typing import List, Dict


# ─────────────────────────────────────────────────────────────────────────────

def get_inference_transform(img_size: int = 224):
    return transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std =[0.229, 0.224, 0.225],
        ),
    ])


def predict_image(
    image,
    model,
    classes: List[str],
    device,
    top_k: int = 5,
    img_size: int = 224,
) -> List[Dict]:
    """
    Run inference on a single PIL image.

    Args:
        image   : PIL.Image or file path string
        model   : loaded PestClassifier (eval mode)
        classes : list of 102 class name strings
        device  : torch device
        top_k   : number of top predictions to return
        img_size: expected input resolution

    Returns:
        List of dicts sorted by confidence (highest first):
        [
          {'rank': 1, 'class_id': 7, 'class_name': '...', 'confidence': 92.3},
          ...
        ]
    """
    transform = get_inference_transform(img_size)

    if isinstance(image, str):
        image = Image.open(image).convert('RGB')
    elif not isinstance(image, Image.Image):
        image = Image.fromarray(image).convert('RGB')

    tensor = transform(image).unsqueeze(0).to(device)   # (1, 3, H, W)

    model.eval()
    with torch.no_grad():
        logits = model(tensor)
        probs  = F.softmax(logits, dim=1)

    top_probs, top_indices = probs.topk(top_k, dim=1)
    top_probs   = top_probs.squeeze().cpu().tolist()
    top_indices = top_indices.squeeze().cpu().tolist()

    # Handle edge case when top_k == 1
    if top_k == 1:
        top_probs   = [top_probs]
        top_indices = [top_indices]

    results = [
        {
            'rank':       rank + 1,
            'class_id':   int(idx),
            'class_name': classes[idx],
            'confidence': round(float(prob) * 100, 2),
        }
        for rank, (prob, idx) in enumerate(zip(top_probs, top_indices))
    ]

    return results
