import streamlit as st
import json
import os

# -------------------------------------------------------
# Load business models JSON
# -------------------------------------------------------
DATA_PATH = "data/business_models.json"

if not os.path.exists(DATA_PATH):
    st.error("❌ Could not find business_models.json in /data/")
    st.stop()

with open(DATA_PATH, "r") as f:
    BUSINESS_MODELS = json.load(f)

st.title("📘 Business Model Library")
st.write("Explore 70 business models with detailed descriptions, examples, risks, and use cases.")


# -------------------------------------------------------
# Tag chip renderer
# -------------------------------------------------------
def tag_chip(tag):
    colors = {
        "software": "#E3F2FD",
        "platform": "#E1F5FE",
        "digital": "#F3E5F5",
        "AI": "#EDE7F6",
        "green": "#E0F2F1",
        "impact": "#FFF3E0",
        "B2B": "#E8F5E9",
        "B2C": "#FFFDE7",
        "low_capex": "#F1F8E9",
        "medium_capex": "#FFF8E1",
        "high_capex": "#FFEBEE",
        "recurring": "#E8EAF6",
        "community": "#E8F5FE",
        "data": "#F3F4F6",
        "manufacturing": "#F9FBE7",
    }
    bg = colors.get(tag, "#F1F1F1")

    return f"""
    <span style="
        background:{bg};
        padding:6px 10px;
        border-radius:8px;
        margin-right:6px;
        font-size:0.8em;
        display:inline-block;
        color:#111;
    ">{tag}</span>
    """


# -------------------------------------------------------
# Helper: bullet list renderer
# -------------------------------------------------------
def bullet_list(items):
    if not items:
        return "<p style='color:#777;font-size:0.85em;'>—</p>"
    html = "<ul style='margin-top:6px;margin-bottom:12px;padding-left:22px;'>"
    for item in items:
        html += f"<li style='margin-bottom:4px;color:#333;font-size:0.9em;'>{item}</li>"
    html += "</ul>"
    return html


# -------------------------------------------------------
# Full card renderer
# -------------------------------------------------------
def render_bm_tile(bm):
    tags_html = " ".join(tag_chip(t) for t in bm.get("tags", []))

    return f"""
<div style="
    background:#FFFFFF;
    border-radius:12px;
    padding:20px;
    border:1px solid #D9D9D9;
    box-shadow:0 2px 10px rgba(0,0,0,0.05);
    margin-bottom:28px;
    color:#222;
    line-height:1.45;
">

    <h3 style="margin-bottom:4px;color:#111;">{bm['name']}</h3>
    <span style="color:#666;font-size:0.85em;">{bm['id']}</span>

    <p style="margin-top:12px;color:#333;">
        {bm['description']}
    </p>

    <div style="margin:12px 0;">{tags_html}</div>

    <div style="
        display:flex;
        justify-content:space-between;
        font-size:0.85em;
        color:#444;
        margin-top:10px;
    ">
        <div><strong>Difficulty:</strong> {bm.get('difficulty','-')}/5</div>
        <div><strong>Capex:</strong> {bm.get('capital_requirement','-')}</div>
    </div>

    <div style="font-size:0.85em;color:#444;margin-top:8px;">
        <strong>Time to Revenue:</strong> {bm.get('time_to_revenue','-')}
    </div>

    <hr style="margin:16px 0;border:0;border-top:1px solid #EEE;">

    <div style="margin-top:8px;">
        <strong style="color:#111;">Revenue Streams</strong>
        {bullet_list(bm.get('revenue_streams', []))}
    </div>

    <div style="margin-top:8px;">
        <strong style="color:#111;">Use Cases</strong>
        {bullet_list(bm.get('use_cases', []))}
    </div>

    <div style="margin-top:8px;">
        <strong style="color:#111;">Examples</strong>
        {bullet_list(bm.get('examples', []))}
    </div>

    <div style="margin-top:8px;">
        <strong style="color:#111;">Risks</strong>
        {bullet_list(bm.get('risks', []))}
    </div>

</div>
"""


# -------------------------------------------------------
# SEARCH + FILTER BAR
# -------------------------------------------------------
st.subheader("🔎 Search & Filter")

search = st.text_input("Search by name, description or tag:", "").lower()

all_tags = sorted({tag for bm in BUSINESS_MODELS for tag in bm.get("tags", [])})

selected_tags = st.multiselect("Filter by tags:", all_tags)


# -------------------------------------------------------
# Filtering logic
# -------------------------------------------------------
filtered = []
for bm in BUSINESS_MODELS:

    # text search
    block = (bm["name"] + " " + bm["description"] + " " + " ".join(bm.get("tags", []))).lower()
    if search and search not in block:
        continue

    # tag filter
    if selected_tags:
        if not set(selected_tags).issubset(set(bm.get("tags", []))):
            continue

    filtered.append(bm)

st.write(f"### {len(filtered)} models found")

# -------------------------------------------------------
# Render models
# -------------------------------------------------------
for bm in filtered:
    st.markdown(render_bm_tile(bm), unsafe_allow_html=True)


