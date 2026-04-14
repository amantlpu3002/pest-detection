"""
app.py  —  Pest Detection System for Farmers
---------------------------------------------
Run with:
    cd app
    streamlit run app.py

Requires:
    - Trained model at ../models/best_model.pth
    - IP102 classes.txt at ../data/ip102/classes.txt
"""

import os
import sys
import streamlit as st
import torch
from PIL import Image
import plotly.graph_objects as go

# ── Path setup ───────────────────────────────────────────────────────────────
APP_DIR   = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR  = os.path.join(APP_DIR, '..')
DATA_DIR  = os.path.join(ROOT_DIR, 'data', 'ip102')
MODEL_DIR = os.path.join(ROOT_DIR, 'models')
CKPT_PATH = os.path.join(MODEL_DIR, 'best_model.pth')

sys.path.insert(0, os.path.abspath(os.path.join(ROOT_DIR, 'src')))

from utils import (
    load_trained_model, load_classes, run_inference,
    DEVICE, SEVERITY_COLORS, SEVERITY_EMOJIS, crop_emoji
)
from pesticide_map import get_pest_info


# ─────────────────────────────────────────────────────────────────────────────
# Page configuration
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌾 Pest Detection System",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Main container ── */
    .main { background-color: #f5f5f0; }

    /* ── Cards ── */
    .pest-card {
        background: white;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 5px solid #2e7d32;
    }
    .pesticide-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
        border-radius: 12px;
        padding: 18px 22px;
        margin-top: 12px;
        border: 1px solid #c8e6c9;
    }
    .warning-card {
        background: #fff8e1;
        border-radius: 10px;
        padding: 14px 18px;
        border-left: 4px solid #f9a825;
        margin-top: 10px;
        font-size: 0.9em;
    }

    /* ── Confidence bar labels ── */
    .conf-label {
        font-size: 0.85em;
        color: #555;
        margin-bottom: 2px;
    }

    /* ── Severity badge ── */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.82em;
        font-weight: 600;
        color: white;
    }

    /* ── Headers ── */
    h1 { color: #1b5e20 !important; }
    h2 { color: #2e7d32 !important; }
    h3 { color: #388e3c !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Cached resources
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner="Loading AI model...")
def get_model_and_classes():
    model   = load_trained_model(CKPT_PATH)
    classes = load_classes(DATA_DIR) if os.path.exists(DATA_DIR) else []
    return model, classes


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://em-content.zobj.net/source/microsoft/378/seedling_1f331.png", width=60)
    st.title("🌾 Pest Detection")
    st.markdown("**AI-powered pest identification for smarter crop protection.**")
    st.divider()

    st.subheader("⚙️ Settings")
    top_k       = st.slider("Top predictions to show", 1, 10, 5)
    conf_thresh = st.slider("Minimum confidence (%)", 0, 100, 10)

    st.divider()
    st.subheader("ℹ️ About")
    st.markdown("""
    - **Model:** EfficientNet-B3
    - **Dataset:** IP102 (102 pest classes)
    - **Framework:** PyTorch
    - **Device:** `{}`
    """.format(str(DEVICE).upper()))

    st.divider()
    st.caption("⚠️ Always consult a certified agronomist before applying pesticides.")


# ─────────────────────────────────────────────────────────────────────────────
# Main page
# ─────────────────────────────────────────────────────────────────────────────
st.title("🐛 Pest Detection System for Farmers")
st.markdown(
    "Upload a crop image to **identify the pest** and receive "
    "**tailored pesticide recommendations** instantly."
)

# Load model
model, classes = get_model_and_classes()

if model is None:
    st.error(
        "⚠️ No trained model found at `models/best_model.pth`. "
        "Please train the model first by running `python src/train.py`."
    )
    st.stop()

if not classes:
    st.error(
        "⚠️ Could not find `data/ip102/classes.txt`. "
        "Please ensure the IP102 dataset is placed correctly."
    )
    st.stop()

st.success(f"✅ Model loaded successfully — {len(classes)} pest classes ready.")

# ── Upload section ────────────────────────────────────────────────────────────
st.subheader("📸 Upload Pest Image")
uploaded = st.file_uploader(
    "Drag and drop or click to upload (JPG, PNG, JPEG)",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed",
)

# ── Demo mode ─────────────────────────────────────────────────────────────────
col_upload, col_demo = st.columns([3, 1])
with col_demo:
    use_demo = st.button("🎲 Try Demo Image", use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# Inference
# ─────────────────────────────────────────────────────────────────────────────
image_to_analyze = None

if uploaded is not None:
    image_to_analyze = Image.open(uploaded).convert('RGB')
elif use_demo:
    # Use a solid-colour placeholder as demo (replace with a real demo image path)
    demo_path = os.path.join(APP_DIR, 'demo.jpg')
    if os.path.exists(demo_path):
        image_to_analyze = Image.open(demo_path).convert('RGB')
    else:
        st.warning("No demo image found. Please place a `demo.jpg` inside the `app/` folder.")

if image_to_analyze is not None:
    st.divider()

    # ── Layout: image | results ───────────────────────────────────────────────
    col_img, col_res = st.columns([1, 2], gap="large")

    with col_img:
        st.subheader("📷 Input Image")
        st.image(image_to_analyze, use_container_width=True, caption="Uploaded crop image")
        st.caption(f"Size: {image_to_analyze.size[0]} × {image_to_analyze.size[1]} px")

    with col_res:
        st.subheader("🔍 Detection Results")

        with st.spinner("Analysing image..."):
            predictions = run_inference(image_to_analyze, model, classes, top_k=top_k)

        # Filter by confidence threshold
        filtered = [p for p in predictions if p['confidence'] >= conf_thresh]

        if not filtered:
            st.warning(
                f"No predictions above {conf_thresh}% confidence. "
                "Try lowering the threshold in the sidebar."
            )
        else:
            # ── Top prediction banner ─────────────────────────────────────────
            top = filtered[0]
            pest_info = get_pest_info(top['class_name'])
            sev   = pest_info.get('severity', 'Unknown')
            sev_c = SEVERITY_COLORS.get(sev, '#95a5a6')
            sev_e = SEVERITY_EMOJIS.get(sev, '⚪')
            c_emoji = crop_emoji(pest_info.get('crop', ''))

            st.markdown(f"""
            <div class="pest-card">
                <h2 style="margin:0 0 6px 0; color:#1b5e20;">
                    🐛 {top['class_name'].title()}
                </h2>
                <p style="margin:0; color:#555; font-size:0.95em;">
                    {pest_info['description']}
                </p>
                <div style="margin-top:12px; display:flex; gap:10px; flex-wrap:wrap;">
                    <span class="badge" style="background:{sev_c};">
                        {sev_e} Severity: {sev}
                    </span>
                    <span class="badge" style="background:#1565c0;">
                        {c_emoji} Crop: {pest_info['crop']}
                    </span>
                    <span class="badge" style="background:#4a148c;">
                        🎯 Confidence: {top['confidence']:.1f}%
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Full-width confidence chart ────────────────────────────────────────────
    st.divider()
    st.subheader("📊 Top Predictions — Confidence Scores")

    names  = [p['class_name'].title() for p in filtered]
    confs  = [p['confidence'] for p in filtered]
    colors = ['#2e7d32' if i == 0 else '#81c784' for i in range(len(confs))]

    fig = go.Figure(go.Bar(
        x=confs,
        y=names,
        orientation='h',
        marker_color=colors,
        text=[f"{c:.1f}%" for c in confs],
        textposition='outside',
    ))
    fig.update_layout(
        xaxis=dict(title='Confidence (%)', range=[0, 110]),
        yaxis=dict(autorange='reversed'),
        height=max(200, len(filtered) * 50 + 60),
        margin=dict(l=10, r=60, t=10, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Pesticide Recommendations ─────────────────────────────────────────────
    st.divider()
    st.subheader("🧪 Pesticide Recommendations")

    top_pest_info = get_pest_info(filtered[0]['class_name'])

    pests_to_show = [p['class_name'] for p in filtered[:3]]
    tab_labels    = [f"#{i+1} {n.title()}" for i, n in enumerate(pests_to_show)]
    tabs          = st.tabs(tab_labels)

    for tab, pred in zip(tabs, filtered[:3]):
        with tab:
            info = get_pest_info(pred['class_name'])

            # Pesticide list
            st.markdown(f"""
            <div class="pesticide-card">
                <h4 style="margin:0 0 10px 0; color:#1b5e20;">
                    💊 Recommended Pesticides
                </h4>
            """, unsafe_allow_html=True)

            for i, p in enumerate(info['pesticides'], 1):
                st.markdown(f"**{i}.** `{p}`")

            st.markdown("</div>", unsafe_allow_html=True)

            # Details table
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🔬 Pesticide Type**")
                st.info(info.get('type', 'N/A'))
                st.markdown("**🌿 Affected Crop**")
                st.info(f"{crop_emoji(info.get('crop',''))} {info.get('crop', 'N/A')}")

            with col2:
                sev = info.get('severity', 'Unknown')
                st.markdown("**⚠️ Severity**")
                st.markdown(
                    f"<span class='badge' style='background:{SEVERITY_COLORS.get(sev,'#95a5a6')};'>"
                    f"{SEVERITY_EMOJIS.get(sev,'⚪')} {sev}</span>",
                    unsafe_allow_html=True
                )
                st.write("")
                st.markdown("**🔍 Description**")
                st.write(info.get('description', 'N/A'))

            # Precaution
            st.markdown(f"""
            <div class="warning-card">
                ⚠️ <strong>Safety Precaution:</strong> {info.get('precaution', '')}
            </div>
            """, unsafe_allow_html=True)

    # ── General safety notice ────────────────────────────────────────────────
    st.divider()
    st.markdown("""
    > **📋 Disclaimer:** Pesticide recommendations are for informational purposes only.
    > Always read the product label, follow local regulations, and consult a certified
    > agronomist or plant protection officer before applying any pesticide.
    > Use recommended Personal Protective Equipment (PPE) during application.
    """)

else:
    # ── Placeholder ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        background:white; border-radius:16px; padding:60px;
        text-align:center; border: 2px dashed #a5d6a7; margin-top:20px;
    ">
        <div style="font-size:4em;">🌿</div>
        <h3 style="color:#2e7d32; margin:12px 0 6px 0;">Upload a crop image to get started</h3>
        <p style="color:#777; font-size:0.95em;">
            Supports JPG, PNG, and JPEG images.<br>
            The AI will identify the pest and suggest appropriate pesticides.
        </p>
    </div>
    """, unsafe_allow_html=True)
