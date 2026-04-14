# 🌾 Pest Detection System for Farmers
## IP102 Dataset | PyTorch | EfficientNet-B3 | Streamlit

---

## 📁 Project Structure

```
pest_detection/
├── data/
│   └── ip102/                  ← Place your IP102 dataset here
│       ├── classification/
│       │   ├── train/
│       │   ├── val/
│       │   └── test/
│       ├── classes.txt
│       ├── train.txt
│       ├── val.txt
│       └── test.txt
├── src/
│   ├── dataset.py              ← Dataset & DataLoader
│   ├── model.py                ← EfficientNet-B3 model
│   ├── train.py                ← Training script
│   ├── evaluate.py             ← Evaluation & metrics
│   └── predict.py              ← Inference utilities
├── app/
│   ├── app.py                  ← Streamlit web application
│   ├── utils.py                ← Helper functions
│   └── pesticide_map.py        ← Pest → Pesticide mapping
├── models/                     ← Saved model checkpoints
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

```bash
# 1. Clone / download project
cd pest_detection

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Place IP102 dataset inside data/ip102/
```

---

## 🏋️ Training

```bash
cd src
python train.py
```
- Trains EfficientNet-B3 with transfer learning
- Handles class imbalance via weighted loss
- Saves best model to `models/best_model.pth`

---

## 📊 Evaluation

```bash
cd src
python evaluate.py
```
- Reports Top-1 and Top-5 accuracy
- Generates classification report
- Saves training curves

---

## 🚀 Run Web App

```bash
cd app
streamlit run app.py
```
- Upload a pest image
- Get pest name + confidence score
- Get pesticide recommendation

---

## 🧠 Model

| Property        | Value               |
|----------------|---------------------|
| Backbone        | EfficientNet-B3     |
| Pretrained      | ImageNet            |
| Input Size      | 224 × 224           |
| Output Classes  | 102                 |
| Optimizer       | AdamW               |
| Scheduler       | CosineAnnealingLR   |
| Loss Function   | Weighted CrossEntropy|

---

## 📦 Requirements
See `requirements.txt`
