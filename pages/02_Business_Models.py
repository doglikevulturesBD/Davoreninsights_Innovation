import streamlit as st
import json
import os

st.title("Business Model Explorer")

# ---------------------------------------------------
# Load JSON
# ---------------------------------------------------
DATA_PATH = "data/business_models.json"

if not os.path.exists(DATA_PATH):
    st.error("❌ Could not find business_models.json in /data")
    st.stop()

with open(DATA_PATH, "r") as f:
    BUSINESS_MODELS = json.load(f)


# ---------------------------------------------------
# Helper functions
# ---------------------------------------------------
def tag_chip(tag):
    """Return a styled tag bubble."""
    colors = {
        "software": "#E8EAF6",
        "platform": "#E1F5FE",
        "digital": "#F3E5F5",
        "AI": "#E8F5E9",
        "green": "#E0F2F1",
    }
    bg = colors.get(tag, "#EFEFEF")
    return f"""
    <span style="
        background:{bg};
        padding:6px 10px;
        border-radius:8px;
        margin-right:6px;
        font-size:0.8em;
        display:inline-block;
    ">{tag}</span>
    """


def bullet_list(items):
    if not items:
        return "<p style='color:#777;'>None listed</p>"
    html = "<ul style='margin-top:6px;margin-bottom:12px;padding-left:20px;'>"
    for it in items:
        html += f"<li style='margin-bottom:4px;'>{it}</li>"
    html += "</ul>"
    return html


def render_bm_tile(bm):
    """Return full HTML card for one business model."""
    name = bm["name"]
    desc = bm["description"]

    tags_html = " ".join(tag_chip(t) for t in bm['tags'])

    difficulty = bm.get("difficulty", "-")
    capex = bm.get("capital_requirement", "-")
    ttr = bm.get("time_to_revenue", "-")

    rev = bm.get("revenue_streams", [])
    use = bm.get("use_cases", [])
    examples = bm.get("examples", [])
    risks = bm.get("risks", [])

    return f"""
<div style="
    background:#ffffff;
    border-radius:12px;
    padding:18px;
    border:1px solid #e5e5e5;
    box-shadow:0 2px 8px rgba(0,0,0,0.06);
    margin-bottom:20px;
">

    <h3 style="margin-bottom:4px;">{name}</h3>
    <span style="color:#888;font-size:0.85em;">{bm['id']}</span>

    <p style="margin-top:12px;color:#444;">{desc}</p>

    <div style="margin:12px 0;">{tags_html}</div>

    <div style="
        display:flex;
        justify-content:space-between;
        font-size:0.8em;
        color:#444;
        margin-top:10px;
    ">
        <div><strong>Difficulty:</strong> {difficulty}/5</div>
        <div><strong>Capex:</strong> {capex}</div>
    </div>

    <div style="font-size:0.8em;color:#444;margin-top:4px;">
        <strong>Time to Revenue:</strong> {ttr}
    </div>

    <hr style="margin:14px 0;">

    <div style="margin-top:8px;">
        <strong>Revenue Streams</strong>
        {bullet_list(rev)}
    </div>

    <div style="margin-top:8px;">
        <strong>Use Cases</strong>
        {bullet_list(use)}
    </div>

    <div style="margin-top:8px;">
        <strong>Example Companies</strong>
        {bullet_list(examples)}
    </div>

    <div style="margin-top:8px;">
        <strong>Risks</strong>
        {bullet_list(risks)}
    </div>

</div>
"""


# ---------------------------------------------------
# Archetype Selection
# ---------------------------------------------------
st.subheader("Choose your Innovator Archetype")

archetypes = [
    "Tech Builder",
    "Ecosystem Architect",
    "Impact Innovator",
    "Commercial Strategist",
    "Creative Entrepreneur"
]

archetype = st.selectbox("Select your profile:", archetypes)

st.markdown("---")
st.subheader(f"Business Models for: **{archetype}**")


# ---------------------------------------------------
# Render All Cards
# ---------------------------------------------------
for bm in BUSINESS_MODELS:
    st.html(render_bm_tile(bm))


