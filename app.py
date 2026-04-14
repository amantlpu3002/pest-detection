"""
app.py — AgroShield Pest Detection System
==========================================
Deployment-ready version with:
- Auto model download from Google Drive
- No hardcoded local paths
- Full error handling
- Works on Streamlit Cloud

Run locally  : streamlit run app.py
Deploy       : Push to GitHub + Streamlit Cloud
"""

import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import timm
import streamlit as st
from PIL import Image
from torchvision import transforms
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# Page config — MUST be first Streamlit call
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AgroShield | Pest Detection",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Paths — work both locally and on Streamlit Cloud
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR      = os.path.join(BASE_DIR, 'models')
MODEL_PATH     = os.path.join(MODEL_DIR, 'best_model.pth')
CLASSES_FILE   = os.path.join(BASE_DIR, 'classes.txt')

# ── PASTE YOUR GOOGLE DRIVE FILE ID HERE ────────────────────────────────────
GDRIVE_FILE_ID = '1zPWQz0H9Ky-hb49nDpy6rRHZUyrph2oV'
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# Auto-download model from Google Drive if not present
# ─────────────────────────────────────────────────────────────────────────────
def download_model_if_needed():
    if os.path.exists(MODEL_PATH):
        return True
    try:
        import gdown
        os.makedirs(MODEL_DIR, exist_ok=True)
        with st.spinner("Downloading AI model (first time only)..."):
            url = f'https://drive.google.com/uc?id={GDRIVE_FILE_ID}'
            gdown.download(url, MODEL_PATH, quiet=False)
        if os.path.exists(MODEL_PATH):
            st.success("Model downloaded successfully!")
            return True
        else:
            st.error("Model download failed. Please check your Google Drive File ID.")
            return False
    except Exception as e:
        st.error(f"Error downloading model: {e}")
        return False

# ─────────────────────────────────────────────────────────────────────────────
# CSS Styling
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main { background: #f7f5f0; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

.hero {
    background: linear-gradient(135deg, #1a3a1a 0%, #2d5a27 50%, #1a3a1a 100%);
    border-radius: 20px;
    padding: 40px 48px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(144,238,144,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3em; font-weight: 900;
    color: #f0f7ee; margin: 0;
    line-height: 1.1; letter-spacing: -1px;
}
.hero-title span { color: #7dd87a; }
.hero-sub {
    color: #a8c8a5; font-size: 1.05em;
    margin-top: 10px; font-weight: 300;
}
.hero-badge {
    display: inline-block;
    background: rgba(125,216,122,0.2);
    border: 1px solid rgba(125,216,122,0.4);
    color: #7dd87a; padding: 4px 14px;
    border-radius: 20px; font-size: 0.78em;
    font-weight: 600; letter-spacing: 1px;
    text-transform: uppercase; margin-bottom: 14px;
}
.result-card {
    background: white; border-radius: 18px;
    padding: 28px 32px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.07);
    border-top: 5px solid #2d5a27;
    margin-bottom: 20px;
}
.pest-name {
    font-family: 'Playfair Display', serif;
    font-size: 2em; font-weight: 700;
    color: #1a3a1a; margin: 0 0 6px 0;
}
.pest-desc {
    color: #5a6b58; font-size: 0.97em;
    line-height: 1.6; margin: 10px 0 0 0;
}
.badge-row { display: flex; gap: 10px; flex-wrap: wrap; margin: 14px 0; }
.badge {
    display: inline-flex; align-items: center;
    gap: 5px; padding: 5px 14px;
    border-radius: 30px; font-size: 0.82em;
    font-weight: 600; letter-spacing: 0.3px;
}
.badge-high   { background:#fff0f0; color:#c0392b; border:1px solid #f5c6c6; }
.badge-medium { background:#fff8e6; color:#d68910; border:1px solid #fde8a0; }
.badge-low    { background:#edfaed; color:#27ae60; border:1px solid #b7e5b7; }
.badge-crop   { background:#eef4ff; color:#2471a3; border:1px solid #adc8f0; }
.badge-conf   { background:#f0eeff; color:#6c3483; border:1px solid #d2b4f5; }
.pest-card {
    background: linear-gradient(135deg, #f0f9f0 0%, #e8f5e8 100%);
    border-radius: 14px; padding: 22px 26px;
    border: 1px solid #c3e0c0; margin-top: 16px;
}
.pest-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15em; color: #1a3a1a;
    margin: 0 0 14px 0; font-weight: 700;
}
.pesticide-item {
    background: white; border-radius: 10px;
    padding: 10px 16px; margin: 8px 0;
    border-left: 4px solid #2d5a27;
    font-size: 0.92em; color: #1a3a1a;
    font-weight: 500;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.warning-box {
    background: #fffbf0; border-radius: 12px;
    padding: 14px 18px;
    border: 1px solid #fde8a0;
    border-left: 4px solid #f39c12;
    margin-top: 14px; font-size: 0.88em;
    color: #7d6608; line-height: 1.5;
}
.stat-box {
    background: white; border-radius: 14px;
    padding: 20px; text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.2em; font-weight: 900;
    color: #2d5a27; line-height: 1;
}
.stat-label {
    color: #8a9e88; font-size: 0.8em;
    font-weight: 500; text-transform: uppercase;
    letter-spacing: 0.8px; margin-top: 4px;
}
.img-container {
    background: white; border-radius: 16px;
    padding: 14px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}
.placeholder {
    background: white; border-radius: 20px;
    padding: 80px 40px; text-align: center;
    border: 2px dashed #c8dbc5; margin-top: 10px;
}
.placeholder-icon { font-size: 4.5em; margin-bottom: 16px; }
.placeholder-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.6em; color: #2d5a27; margin-bottom: 8px;
}
.placeholder-sub { color: #8a9e88; font-size: 0.95em; }
.disclaimer {
    background: #f0f7f0; border-radius: 12px;
    padding: 14px 20px; border: 1px solid #c8dbc5;
    font-size: 0.83em; color: #5a6b58;
    line-height: 1.6; margin-top: 24px;
}
section[data-testid="stSidebar"] { background: #1a3a1a; }
section[data-testid="stSidebar"] * { color: #c8dbc5 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Pesticide Map
# ─────────────────────────────────────────────────────────────────────────────
PESTICIDE_MAP = {
    "rice leaf roller":          {"pesticides": ["Chlorpyrifos 20 EC", "Monocrotophos 36 SL", "Cartap 50 SP"],        "severity": "High",   "crop": "Rice",       "type": "Organophosphate",    "desc": "Larvae roll rice leaves and feed inside, reducing photosynthesis.",            "precaution": "Apply in the evening. Avoid during flowering stage."},
    "rice leaf caterpillar":     {"pesticides": ["Chlorantraniliprole 18.5 SC", "Flubendiamide 39.35 SC"],            "severity": "Medium", "crop": "Rice",       "type": "Diamide insecticide","desc": "Caterpillars feed on rice leaves causing white streaks and defoliation.",       "precaution": "Rotate insecticide classes to prevent resistance."},
    "paddy stem maggot":         {"pesticides": ["Carbofuran 3 G", "Phorate 10 G", "Chlorpyrifos 20 EC"],             "severity": "High",   "crop": "Rice",       "type": "Carbamate",          "desc": "Maggots bore into rice stems causing dead heart symptoms.",                    "precaution": "Apply granules at root zone. Avoid contact with skin."},
    "asiatic rice borer":        {"pesticides": ["Cartap Hydrochloride 4 G", "Fipronil 0.3 G"],                       "severity": "High",   "crop": "Rice",       "type": "Nereistoxin analogue","desc": "Major rice borer causing dead heart and white ear symptoms.",                 "precaution": "Apply at early infestation. Drain fields before application."},
    "yellow rice borer":         {"pesticides": ["Fipronil 5 SC", "Chlorpyrifos 20 EC", "Triazophos 40 EC"],          "severity": "High",   "crop": "Rice",       "type": "Organophosphate",    "desc": "Most destructive rice stem borer causing spikelet sterility.",                 "precaution": "Monitor pheromone traps for adult moth population."},
    "rice gall midge":           {"pesticides": ["Carbofuran 3 G", "Phorate 10 G"],                                   "severity": "Medium", "crop": "Rice",       "type": "Carbamate",          "desc": "Larvae induce silver shoot formation, destroying the main tiller.",            "precaution": "Apply at tillering stage. Avoid fish pond contamination."},
    "brown plant hopper":        {"pesticides": ["Buprofezin 25 SC", "Imidacloprid 17.8 SL", "Pymetrozine 50 WG"],   "severity": "High",   "crop": "Rice",       "type": "IGR / Neonicotinoid","desc": "Sap-sucking pest causing hopperburn; vector of grassy stunt virus.",           "precaution": "Do not use pyrethroids — they cause hopper resurgence."},
    "white backed plant hopper": {"pesticides": ["Buprofezin 25 SC", "Ethofenprox 10 EC"],                            "severity": "High",   "crop": "Rice",       "type": "IGR insecticide",    "desc": "Transmits rice stripe and black-streaked dwarf viruses.",                      "precaution": "Apply at base of plant. Maintain field water level."},
    "rice water weevil":         {"pesticides": ["Carbofuran 3 G", "Fipronil 0.3 G"],                                 "severity": "Medium", "crop": "Rice",       "type": "Carbamate",          "desc": "Larvae attack rice roots reducing plant vigour.",                              "precaution": "Apply granules to flooded paddies. Harmful to aquatic organisms."},
    "corn borer":                {"pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG"],           "severity": "High",   "crop": "Corn",       "type": "Diamide insecticide","desc": "Larvae bore into corn stalks and ears causing up to 20% yield loss.",          "precaution": "Apply at whorl stage. Avoid spraying during flowering."},
    "black cutworm":             {"pesticides": ["Lambda-cyhalothrin 5 EC", "Chlorpyrifos 20 EC"],                    "severity": "High",   "crop": "Corn",       "type": "Pyrethroid",         "desc": "Cuts young seedlings at soil level causing stand loss.",                       "precaution": "Apply at soil surface around plant base. Active at night."},
    "beet armyworm":             {"pesticides": ["Spinosad 45 SC", "Indoxacarb 14.5 SC", "Methomyl 90 SP"],          "severity": "High",   "crop": "Beet / Corn","type": "Spinosyn",           "desc": "Fast-developing caterpillar that develops resistance rapidly.",                "precaution": "Rotate insecticide modes of action every generation."},
    "fall armyworm":             {"pesticides": ["Emamectin Benzoate 5 SG", "Chlorantraniliprole 18.5 SC"],           "severity": "High",   "crop": "Corn",       "type": "Macrolide / Diamide","desc": "Highly invasive pest causing devastating crop losses globally.",               "precaution": "Apply at early whorl stage. Use pheromone traps for monitoring."},
    "corn earworm":              {"pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG"],           "severity": "High",   "crop": "Corn",       "type": "Diamide",            "desc": "Polyphagous pest attacking corn, tomato, cotton and soybean.",                 "precaution": "Apply to corn silks. Monitor with pheromone traps."},
    "aphid":                     {"pesticides": ["Imidacloprid 17.8 SL", "Pirimicarb 50 WG", "Flonicamid 50 WG"],   "severity": "Medium", "crop": "General",    "type": "Neonicotinoid",      "desc": "Sap-sucking insects causing stunting and virus transmission.",                 "precaution": "Preserve natural enemies. Avoid broad-spectrum sprays."},
    "boll weevil":               {"pesticides": ["Malathion 50 EC", "Chlorpyrifos 20 EC", "Spinosad 45 SC"],         "severity": "High",   "crop": "Cotton",     "type": "Organophosphate",    "desc": "Larvae develop inside cotton bolls causing boll drop.",                       "precaution": "Use pheromone traps for monitoring. Destroy crop residues."},
    "cotton bollworm":           {"pesticides": ["Emamectin Benzoate 5 SG", "Chlorantraniliprole 18.5 SC"],          "severity": "High",   "crop": "Cotton",     "type": "Macrolide",          "desc": "One of the most economically important pests worldwide.",                      "precaution": "Monitor egg counts. Use Bt-cotton varieties."},
    "whitefly":                  {"pesticides": ["Spirotetramat 15 OD", "Buprofezin 25 SC", "Thiamethoxam 25 WG"],   "severity": "High",   "crop": "Tomato",     "type": "Lipid biosynthesis", "desc": "Vector of begomoviruses. Honeydew causes sooty mould.",                        "precaution": "Yellow sticky traps for monitoring. Introduce Encarsia."},
    "diamondback moth":          {"pesticides": ["Spinosad 45 SC", "Chlorantraniliprole 18.5 SC", "Bt"],             "severity": "High",   "crop": "Cabbage",    "type": "Spinosyn",           "desc": "Most resistant pest globally; skeletonises brassica leaves.",                  "precaution": "Strict rotation of insecticide classes essential."},
    "spider mite":               {"pesticides": ["Abamectin 1.8 EC", "Bifenazate 24 SC", "Hexythiazox 5 EC"],        "severity": "High",   "crop": "General",    "type": "Acaricide",          "desc": "Causes stippling and bronzing; thrives in hot dry conditions.",                "precaution": "Rotate miticide classes. Avoid pyrethroid use."},
    "thrips":                    {"pesticides": ["Spinosad 45 SC", "Imidacloprid 17.8 SL", "Abamectin 1.8 EC"],     "severity": "Medium", "crop": "Vegetables", "type": "Spinosyn",           "desc": "Tiny insects causing silvery streaking; vector of tospoviruses.",              "precaution": "Blue sticky traps for monitoring."},
    "codling moth":              {"pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG"],          "severity": "High",   "crop": "Apple",      "type": "Diamide",            "desc": "Larvae bore into apple core; major orchard pest globally.",                   "precaution": "Begin sprays at petal fall. Use pheromone traps for timing."},
    "japanese beetle":           {"pesticides": ["Imidacloprid 600 FS", "Chlorantraniliprole 18.5 SC"],              "severity": "High",   "crop": "Rose / Grape","type": "Neonicotinoid",     "desc": "Adults skeletonise leaves; grubs damage turf roots.",                          "precaution": "Pheromone traps attract more beetles — place away from crops."},
    "tobacco hornworm":          {"pesticides": ["Spinosad 45 SC", "Bt (Bacillus thuringiensis)", "Chlorantraniliprole 18.5 SC"], "severity": "High", "crop": "Tobacco / Tomato", "type": "Spinosyn", "desc": "Large caterpillar that defoliates plants rapidly.",            "precaution": "Hand-pick where populations are low. Bt is organic-approved."},
    "tomato fruitworm":          {"pesticides": ["Chlorantraniliprole 18.5 SC", "Emamectin Benzoate 5 SG"],          "severity": "High",   "crop": "Tomato",     "type": "Diamide",            "desc": "Bores into tomato fruit causing internal decay.",                              "precaution": "Begin sprays when eggs first detected on leaves."},
    "potato leafhopper":         {"pesticides": ["Imidacloprid 17.8 SL", "Carbaryl 85 WP", "Malathion 50 EC"],      "severity": "High",   "crop": "Potato",     "type": "Neonicotinoid",      "desc": "Causes hopperburn — marginal leaf scorch and curling.",                        "precaution": "Apply preventively as damage occurs before symptoms appear."},
    "hessian fly":               {"pesticides": ["Chlorpyrifos 20 EC", "Dimethoate 30 EC"],                          "severity": "High",   "crop": "Wheat",      "type": "Organophosphate",    "desc": "Larvae stunt wheat plants; major wheat pest.",                                "precaution": "Fly-free planting dates most effective. Use resistant varieties."},
    "grub":                      {"pesticides": ["Chlorpyrifos 20 EC", "Phorate 10 G", "Imidacloprid 600 FS"],       "severity": "High",   "crop": "General",    "type": "Organophosphate",    "desc": "White grubs feed on roots causing wilting and plant death.",                   "precaution": "Soil drench at planting. Highly toxic — use full PPE."},
    "cutworm":                   {"pesticides": ["Chlorpyrifos 20 EC", "Lambda-cyhalothrin 5 EC", "Spinosad 45 SC"],"severity": "High",   "crop": "Vegetables", "type": "Organophosphate",    "desc": "Nocturnal caterpillars cutting seedlings at ground level.",                   "precaution": "Bait applications at dusk. Tillage exposes larvae to birds."},
    "red spider":                {"pesticides": ["Abamectin 1.8 EC", "Spiromesifen 22.9 SC", "Hexythiazox 5 EC"],   "severity": "High",   "crop": "Vegetables", "type": "Acaricide",          "desc": "Spider mites suck cell contents causing bronzing and leaf drop.",              "precaution": "Rotate miticides. Ensure thorough coverage of leaf undersides."},
}

SEVERITY_STYLE = {
    "High":    ("badge-high",   "🔴"),
    "Medium":  ("badge-medium", "🟡"),
    "Low":     ("badge-low",    "🟢"),
    "Unknown": ("badge-low",    "⚪"),
}

def get_pest_info(name):
    name_lower = name.lower()
    # Remove class number prefix if present (e.g. "12 rice leafhopper" → "rice leafhopper")
    parts = name_lower.split(' ', 1)
    if parts[0].isdigit() and len(parts) > 1:
        name_lower = parts[1].strip()
    if name_lower in PESTICIDE_MAP:
        return PESTICIDE_MAP[name_lower]
    for key, val in PESTICIDE_MAP.items():
        if key in name_lower or name_lower in key:
            return val
    return {
        "pesticides": ["Consult local agricultural extension officer"],
        "severity":   "Unknown",
        "crop":       "Unknown",
        "type":       "Unknown",
        "desc":       f"Pest identified as '{name}'. Please consult a certified agronomist for treatment advice.",
        "precaution": "Always wear PPE when applying any pesticide.",
    }

# ─────────────────────────────────────────────────────────────────────────────
# Model Definition
# ─────────────────────────────────────────────────────────────────────────────
class PestClassifier(nn.Module):
    def __init__(self, num_classes=102, dropout=0.3):
        super().__init__()
        self.backbone   = timm.create_model(
            'efficientnet_b3', pretrained=False,
            num_classes=0, global_pool='avg'
        )
        in_features     = self.backbone.num_features
        self.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout / 2),
            nn.Linear(512, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.backbone(x))


@st.cache_resource(show_spinner=False)
def load_model_and_classes():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # ── Load class names ─────────────────────────────────────────
    if not os.path.exists(CLASSES_FILE):
        st.error(f"classes.txt not found at {CLASSES_FILE}")
        st.stop()

    with open(CLASSES_FILE, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # ── Load model ───────────────────────────────────────────────
    if not os.path.exists(MODEL_PATH):
        st.error("Model file not found! Make sure best_model.pth is in models/ folder.")
        st.stop()

    model = PestClassifier(num_classes=len(classes)).to(device)
    ckpt  = torch.load(MODEL_PATH, map_location=device)
    model.load_state_dict(ckpt['model_state_dict'])
    model.eval()

    return model, classes, device, ckpt.get('val_acc', 69.89), ckpt.get('epoch', 30)


def predict_with_tta(image: Image.Image, model, classes, device, top_k=5):
    """
    Test Time Augmentation — predict 5 augmented versions and average.
    Improves accuracy by 2-3% over single prediction.
    """
    base = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    tta_transforms = [
        base,
        transforms.Compose([transforms.Resize((224,224)), transforms.RandomHorizontalFlip(p=1.0), transforms.ToTensor(), transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])]),
        transforms.Compose([transforms.Resize((256,256)), transforms.CenterCrop(224),              transforms.ToTensor(), transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])]),
        transforms.Compose([transforms.Resize((224,224)), transforms.RandomRotation((10,10)),       transforms.ToTensor(), transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])]),
        transforms.Compose([transforms.Resize((224,224)), transforms.ColorJitter(brightness=0.2),  transforms.ToTensor(), transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])]),
    ]
    all_probs = []
    model.eval()
    with torch.no_grad():
        for t in tta_transforms:
            tensor = t(image).unsqueeze(0).to(device)
            probs  = F.softmax(model(tensor), dim=1)
            all_probs.append(probs)

    avg_probs    = torch.stack(all_probs).mean(0)
    top_p, top_i = avg_probs.topk(top_k, dim=1)
    top_p = top_p.squeeze().cpu().tolist()
    top_i = top_i.squeeze().cpu().tolist()
    if top_k == 1:
        top_p, top_i = [top_p], [top_i]

    return [{'rank': r+1, 'class_id': int(i),
             'class_name': classes[i],
             'confidence': round(float(p)*100, 2)}
            for r, (p, i) in enumerate(zip(top_p, top_i))]


# ─────────────────────────────────────────────────────────────────────────────
# Download model if needed (for cloud deployment)
# ─────────────────────────────────────────────────────────────────────────────
if not os.path.exists(MODEL_PATH):
    if GDRIVE_FILE_ID == 'YOUR_GOOGLE_DRIVE_FILE_ID_HERE':
        st.error("Please set your GDRIVE_FILE_ID in app.py before deploying!")
        st.stop()
    success = download_model_if_needed()
    if not success:
        st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 AgroShield")
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    top_k       = st.slider("Top predictions", 1, 10, 5)
    conf_thresh = st.slider("Min confidence (%)", 0, 50, 5)
    use_tta     = st.checkbox("Use TTA (better accuracy)", value=True)
    st.markdown("---")
    st.markdown("### 📷 Photo Tips")
    st.markdown("""
    For best results:
    - ✅ Close-up of the pest
    - ✅ Pest clearly visible
    - ✅ Good natural lighting
    - ✅ Steady clear photo
    - ❌ Avoid blurry images
    - ❌ Avoid dark photos
    - ❌ Avoid far away shots
    """)
    st.markdown("---")
    st.markdown("### ℹ️ Model Info")
    st.markdown("""
    - **Model:** EfficientNet-B3
    - **Dataset:** IP102
    - **Classes:** 102 pest types
    - **Top-1 Acc:** 69.35%
    - **Top-5 Acc:** 88.20%
    """)
    st.markdown("---")
    st.caption("⚠️ Always consult a certified agronomist before applying pesticides.")


# ─────────────────────────────────────────────────────────────────────────────
# Hero Header
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🛡️ AI-Powered Crop Protection</div>
    <div class="hero-title">Agro<span>Shield</span></div>
    <div class="hero-sub">
        Intelligent pest detection for smarter, safer farming —
        powered by EfficientNet-B3 trained on 75,000+ pest images across 102 species
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Load Model
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner("Loading AI model..."):
    model, classes, device, val_acc, best_epoch = load_model_and_classes()

# ─────────────────────────────────────────────────────────────────────────────
# Stats Row
# ─────────────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""<div class="stat-box">
        <div class="stat-value">102</div>
        <div class="stat-label">Pest Classes</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="stat-box">
        <div class="stat-value">69%</div>
        <div class="stat-label">Top-1 Accuracy</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="stat-box">
        <div class="stat-value">88%</div>
        <div class="stat-label">Top-5 Accuracy</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown("""<div class="stat-box">
        <div class="stat-value">75K+</div>
        <div class="stat-label">Training Images</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Upload
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("### 📸 Upload Pest Image")
uploaded = st.file_uploader(
    "Upload a clear image of the pest or affected crop",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

# ─────────────────────────────────────────────────────────────────────────────
# Inference
# ─────────────────────────────────────────────────────────────────────────────
if uploaded is None:
    st.markdown("""
    <div class="placeholder">
        <div class="placeholder-icon">🌾</div>
        <div class="placeholder-title">Upload a pest image to get started</div>
        <div class="placeholder-sub">
            Supports JPG, PNG and JPEG formats<br>
            For best results use a clear close-up photo of the pest
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    image = Image.open(uploaded).convert('RGB')

    with st.spinner("Analysing image with AI..."):
        preds = predict_with_tta(image, model, classes, device, top_k=top_k) \
                if use_tta else \
                [{'rank': r+1, 'class_id': int(i), 'class_name': classes[i],
                  'confidence': round(float(p)*100, 2)}
                 for r, (p, i) in enumerate(zip(
                     *[x.squeeze().cpu().tolist() for x in
                       F.softmax(model(
                           transforms.Compose([
                               transforms.Resize((224,224)),
                               transforms.ToTensor(),
                               transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
                           ])(image).unsqueeze(0).to(device), dim=1
                       ).topk(top_k, dim=1)]))]

    preds = [p for p in preds if p['confidence'] >= conf_thresh]

    if not preds:
        st.warning(f"No predictions above {conf_thresh}% confidence. Lower the threshold in the sidebar.")
        st.stop()

    top  = preds[0]
    info = get_pest_info(top['class_name'])
    sev  = info.get('severity', 'Unknown')
    sev_class, sev_emoji = SEVERITY_STYLE.get(sev, ("badge-low", "⚪"))

    # ── Confidence Warning ────────────────────────────────────────
    top_conf = top['confidence']
    if top_conf < 30:
        st.error("⚠️ Very low confidence — please upload a clearer, closer photo of the pest.")
    elif top_conf < 50:
        st.warning("🟡 Moderate confidence — check Top-5 predictions and consult an agronomist.")
    else:
        st.success(f"✅ High confidence prediction ({top_conf:.1f}%)")

    # ── Layout ───────────────────────────────────────────────────
    col_img, col_res = st.columns([1, 1.6], gap="large")

    with col_img:
        st.markdown("#### Input Image")
        st.markdown('<div class="img-container">', unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption(f"Size: {image.size[0]} × {image.size[1]} px")

    with col_res:
        st.markdown("#### Detection Result")
        st.markdown(f"""
        <div class="result-card">
            <div class="pest-name">🐛 {top['class_name'].title()}</div>
            <div class="badge-row">
                <span class="badge {sev_class}">{sev_emoji} {sev} Severity</span>
                <span class="badge badge-crop">🌿 {info['crop']}</span>
                <span class="badge badge-conf">🎯 {top['confidence']}% Confidence</span>
            </div>
            <div class="pest-desc">{info['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="pest-card">
            <div class="pest-card-title">💊 Recommended Pesticides</div>
        """, unsafe_allow_html=True)
        for i, p in enumerate(info['pesticides'], 1):
            st.markdown(f'<div class="pesticide-item">#{i} &nbsp; {p}</div>',
                        unsafe_allow_html=True)
        st.markdown(f"""
            <div class="warning-box">
                ⚠️ <strong>Safety Precaution:</strong> {info['precaution']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Confidence Chart ─────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📊 Top Predictions — Confidence Scores")

    names  = [p['class_name'].title() for p in preds]
    confs  = [p['confidence'] for p in preds]
    colors = ['#2d5a27' if i == 0 else '#7dd87a' for i in range(len(confs))]

    fig = go.Figure(go.Bar(
        x=confs, y=names, orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        text=[f"{c:.1f}%" for c in confs],
        textposition='outside',
        textfont=dict(size=12, color='#1a3a1a'),
    ))
    fig.update_layout(
        xaxis=dict(title='Confidence (%)', range=[0, 115],
                   gridcolor='#e8f0e8'),
        yaxis=dict(autorange='reversed',
                   tickfont=dict(color='#1a3a1a', size=12)),
        height=max(220, len(preds) * 52 + 60),
        margin=dict(l=10, r=80, t=20, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(247,245,240,0.5)',
        font=dict(family='DM Sans'),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Other predictions tabs ────────────────────────────────────
    if len(preds) > 1:
        st.markdown("---")
        st.markdown("### 🔎 Other Possible Pests")
        tab_labels = [f"#{p['rank']} {p['class_name'].title()} ({p['confidence']}%)"
                      for p in preds[1:4]]
        tabs = st.tabs(tab_labels)
        for tab, pred in zip(tabs, preds[1:4]):
            with tab:
                info2 = get_pest_info(pred['class_name'])
                sev2  = info2.get('severity', 'Unknown')
                _, se2 = SEVERITY_STYLE.get(sev2, ("badge-low", "⚪"))
                ca, cb = st.columns(2)
                with ca:
                    st.markdown("**Description**")
                    st.info(info2['desc'])
                    st.markdown(f"**Affected Crop:** {info2['crop']}")
                with cb:
                    st.markdown(f"**Severity:** {se2} {sev2}")
                    st.markdown(f"**Pesticide Type:** {info2['type']}")
                    st.markdown("**Recommended Pesticides:**")
                    for p in info2['pesticides']:
                        st.markdown(f"- `{p}`")
                st.markdown(f"> ⚠️ **Precaution:** {info2['precaution']}")

    # ── Disclaimer ────────────────────────────────────────────────
    st.markdown("""
    <div class="disclaimer">
        📋 <strong>Disclaimer:</strong> Pesticide recommendations are for
        informational purposes only. Always read the product label, follow
        local regulations, and consult a certified agronomist before applying
        any pesticide. Use appropriate Personal Protective Equipment (PPE).
    </div>
    """, unsafe_allow_html=True)