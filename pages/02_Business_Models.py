import streamlit as st
import json
import re

# -------------------------------------------------------------------
# Load Data
# -------------------------------------------------------------------
with open("data/business_models.json", "r") as f:
    BUSINESS_MODELS = json.load(f)

with open("data/archetype_tags.json", "r") as f:
    ARCHETYPES = json.load(f)

# Weight map
MATURITY_MAP = {"emerging": 0.3, "established": 0.6, "dominant": 1.0}

# -------------------------------------------------------------------
# Helper: Format Tag Chip
# -------------------------------------------------------------------
def tag_chip(tag):
    """Return an HTML tag chip with colour coding."""
    # simple colour categories
    colour_map = {
        "AI": "#E3F2FD",
        "software": "#FFF3E0",
        "platform": "#E8EAF6",
        "impact": "#E8F5E9",
        "green": "#E8F5E9",
        "B2B": "#E1F5FE",
        "B2C": "#FCE4EC",
        "digital": "#F3E5F5",
        "research": "#E0F7FA",
    }

    bg = colour_map.get(tag, "#EFEFEF")
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

# -------------------------------------------------------------------
# Helper: Scoring Function
# -------------------------------------------------------------------
def score_model(model, archetype_tags):
    overlap = len(set(model["tags"]) & set(archetype_tags))
    tag_score = overlap / max(len(model["tags"]), 1)

    maturity_score = MATURITY_MAP.get(model.get("maturity_level", "established"), 0.6)
    base_success = model.get("success_score", 0.6)

    return (0.5 * tag_score) + (0.3 * base_success) + (0.2 * maturity_score)

# -------------------------------------------------------------------
# Helper: Create Business Model Tile
# -------------------------------------------------------------------
def render_bm_tile(bm):
    name = bm["name"]
    desc = bm["description"]

    tags_html = " ".join(tag_chip(t) for t in bm['tags'])

    difficulty = bm.get("difficulty", "-")
    capex = bm.get("capital_requirement", "-")
    ttr = bm.get("time_to_revenue", "-")

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

        <p style="margin-top:12px;color:#444;">
            {desc}
        </p>

        <div style="margin:12px 0;">
            {tags_html}
        </div>

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

        <div style="
            font-size:0.8em;
            color:#444;
            margin-top:4px;
        ">
            <strong>Time to Revenue:</strong> {ttr}
        </div>

    </div>
    """

# -------------------------------------------------------------------
# Streamlit UI
# -------------------------------------------------------------------
st.title("Business Models — Learning & Recommendation")

# Maintain session state
if "archetype_selected" not in st.session_state:
    st.session_state["archetype_selected"] = False


# -------------------------------------------------------------------
# Step 1: Choose Archetype
# -------------------------------------------------------------------
st.subheader("1. Choose Your Innovator Archetype")

if not st.session_state["archetype_selected"]:
    archetype_choice = st.radio(
        "Select your innovator profile:",
        list(ARCHETYPES.keys())
    )

    if st.button("Continue"):
        st.session_state["archetype"] = archetype_choice
        st.session_state["archetype_selected"] = True
        st.rerun()

else:
    archetype = st.session_state["archetype"]
    st.success(f"Archetype selected: **{archetype}**")
    archetype_tags = ARCHETYPES[archetype]


# -------------------------------------------------------------------
# Step 2: Recommendations
# -------------------------------------------------------------------
if st.session_state["archetype_selected"]:
    st.subheader("2. Recommended Business Models (Top 5)")

    scored = [
        (bm, score_model(bm, archetype_tags))
        for bm in BUSINESS_MODELS
    ]

    scored = sorted(scored, key=lambda x: x[1], reverse=True)
    top5 = scored[:5]

    for bm, score in top5:
        st.markdown(render_bm_tile(bm), unsafe_allow_html=True)


# -------------------------------------------------------------------
# Step 3: Explore All 70 Models
# -------------------------------------------------------------------
st.subheader("3. Explore All 70 Business Models")

with st.expander("Show All Business Models"):
    for bm in BUSINESS_MODELS:
        st.markdown(render_bm_tile(bm), unsafe_allow_html=True)

