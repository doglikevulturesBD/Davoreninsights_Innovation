import streamlit as st
import json
import random

st.title("Business Model Card Viewer")
st.caption("Explore one model at a time — Davoren Insights Edition")

st.markdown("---")

# ----------------------------------
# Load Business Models
# ----------------------------------
with open("data/business_models.json", "r") as f:
    BUSINESS_MODELS = json.load(f)


# ----------------------------------
# Get one model (random or select)
# ----------------------------------
model_names = [bm["name"] for bm in BUSINESS_MODELS]

option = st.selectbox("Choose a business model to view:", ["Random Model"] + model_names)

if option == "Random Model":
    bm = random.choice(BUSINESS_MODELS)
else:
    bm = next(x for x in BUSINESS_MODELS if x["name"] == option)

st.markdown("---")

# ----------------------------------
# FUTURISTIC CARD LAYOUT
# ----------------------------------
st.subheader(bm["name"])
st.write(f"**Model ID:** {bm['id']}")

st.markdown(
    f"""
    <div style="
        padding: 20px;
        border-radius: 12px;
        background-color: rgba(30,30,40,0.8);
        border: 1px solid rgba(100,150,255,0.4);
        box-shadow: 0 0 20px rgba(50,100,200,0.4);
        color: #eee;
    ">
    <h3 style="color:#4CC9F0; margin-top:0;">Overview</h3>
    <p style="font-size:16px;">{bm['description']}</p>

    <h4 style="color:#FFD166;">Tags</h4>
    <p>{", ".join(bm['tags'])}</p>

    <h4 style="color:#FFD166;">Success Score</h4>
    <p>{int(bm['success_score'] * 100)}%</p>

    <h4 style="color:#FFD166;">Maturity Level</h4>
    <p>{bm['maturity_level'].title()}</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")


# ----------------------------------
# MINI-SCENARIOS (FUN + USEFUL)
# ----------------------------------

st.subheader("Micro-Scenarios (What Works / What Fails)")
st.write("These help you understand where this model shines and where it breaks.")

good = st.text_area(
    "✔ When this model works best:",
    placeholder="e.g., SaaS works best when recurring usage is predictable..."
)

bad = st.text_area(
    "❌ When this model fails:",
    placeholder="e.g., fails when user activation is low or onboarding is complex..."
)

st.markdown("---")

# ----------------------------------
# FUTURE BUTTONS
# ----------------------------------
col1, col2 = st.columns(2)

with col1:
    st.button("Next Model (Random)")
with col2:
    st.button("Save Notes (Future Feature)")



