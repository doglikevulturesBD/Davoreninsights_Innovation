import streamlit as st
import json
import os

st.set_page_config(page_title="Business Models", layout="wide")

st.title("Business Model Explorer")
st.write(
    "Use this page to learn different business models in depth. "
    "Start with an archetype to see a focused Top 5, then browse the full library."
)

# -----------------------------
# Load JSON
# -----------------------------
BM_PATH = "data/business_models.json"
ARCH_PATH = "data/archetype_tags.json"

if not os.path.exists(BM_PATH):
    st.error(f"❌ Could not find {BM_PATH}")
    st.stop()

with open(BM_PATH, "r", encoding="utf-8") as f:
    BUSINESS_MODELS = json.load(f)

ARCHETYPE_TAGS = {}
if os.path.exists(ARCH_PATH):
    with open(ARCH_PATH, "r", encoding="utf-8") as f:
        ARCHETYPE_TAGS = json.load(f)


# -----------------------------
# Tag colour system
# -----------------------------
TAG_COLORS = {
    "software": "#E3F2FD",
    "platform": "#E8EAF6",
    "AI": "#FCE4EC",
    "recurring": "#E8F5E9",
    "data": "#FFF3E0",
    "innovation": "#E1F5FE",
    "green": "#E0F2F1",
    "impact": "#FFE0B2",
    "hardware": "#F3E5F5",
    "manufacturing": "#FBE9E7",
    "finance": "#E0F7FA",
    "B2B": "#E8F5E9",
    "B2C": "#FFFDE7",
    "VR": "#F3E5F5",
    "cloud": "#E3F2FD",
    "transaction": "#F1F8E9",
    "low_capex": "#F1F8E9",
    "medium_capex": "#FFF8E1",
    "high_capex": "#FFEBEE",
    "community": "#E3F2FD",
}


def get_tag_color(tag: str) -> str:
    return TAG_COLORS.get(tag, "#EFEFEF")


def tag_chip(tag: str) -> str:
    return f"""
    <span style="
        background:{get_tag_color(tag)};
        padding:6px 10px;
        border-radius:8px;
        margin-right:6px;
        font-size:0.8em;
        display:inline-block;
        color:#111;
    ">{tag}</span>
    """


def bullet_list(items):
    if not items:
        return "<p style='color:#777;font-size:0.85em;'>—</p>"
    html = "<ul style='margin-top:6px;margin-bottom:12px;padding-left:22px;'>"
    for item in items:
        html += (
            f"<li style='margin-bottom:4px;color:#333;font-size:0.9em;'>{item}</li>"
        )
    html += "</ul>"
    return html


# -----------------------------
# HTML tile renderer (card)
# -----------------------------
def render_bm_tile(bm: dict) -> str:
    tags_html = "".join(tag_chip(t) for t in bm.get("tags", []))

    revenue_html = bullet_list(bm.get("revenue_streams", []))
    use_html = bullet_list(bm.get("use_cases", []))
    examples_html = bullet_list(bm.get("examples", []))
    risks_html = bullet_list(bm.get("risks", []))

    difficulty = bm.get("difficulty", "-")
    capex = bm.get("capital_requirement", "-")
    ttr = bm.get("time_to_revenue", "-")

    return f"""
<div style="
    background:#FFFFFF;
    border-radius:12px;
    padding:20px;
    border:1px solid #D9D9D9;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    margin-bottom:24px;
    color:#222;
    line-height:1.45;
">
    <h3 style="margin-bottom:4px;color:#111;">{bm['name']}</h3>
    <span style="color:#666;font-size:0.85em;">{bm['id']}</span>

    <p style="margin-top:12px;color:#333;">
        {bm.get('description','')}
    </p>

    <div style="margin:12px 0;">
        {tags_html}
    </div>

    <div style="
        display:flex;
        justify-content:space-between;
        font-size:0.85em;
        color:#444;
        margin-top:10px;
    ">
        <div><strong>Difficulty:</strong> {difficulty} / 5</div>
        <div><strong>Capex:</strong> {capex}</div>
    </div>

    <div style="font-size:0.85em;color:#444;margin-top:8px;">
        <strong>Time to Revenue:</strong> {ttr}
    </div>

    <hr style="margin:16px 0;border:0;border-top:1px solid #EEE;">

    <div style="margin-top:8px;">
        <strong style="color:#111;">Revenue Streams</strong>
        {revenue_html}
    </div>

    <div style="margin-top:8px;">
        <strong style="color:#111;">Use Cases</strong>
        {use_html}
    </div>

    <div style="margin-top:8px;">
        <strong style="color:#111;">Examples</strong>
        {examples_html}
    </div>

    <div style="margin-top:8px;">
        <strong style="color:#111;">Risks</strong>
        {risks_html}
    </div>
</div>
"""


# -----------------------------
# Simple archetype scoring
# -----------------------------
def score_for_archetype(bm: dict, archetype_tags) -> int:
    """Score by simple tag overlap for now."""
    if not archetype_tags:
        return 0
    return len(set(bm.get("tags", [])) & set(archetype_tags))


# -----------------------------
# SECTION 1: Archetype → Top 5
# -----------------------------
st.markdown("## 1. Archetype-based Top 5")

if ARCHETYPE_TAGS:
    archetype_names = list(ARCHETYPE_TAGS.keys())
    selected_arch = st.selectbox(
        "Choose your innovator archetype:",
        archetype_names,
        index=0,
    )

    arch_tags = ARCHETYPE_TAGS[selected_arch]

    # Compute simple overlap score
    scored = []
    for bm in BUSINESS_MODELS:
        s = score_for_archetype(bm, arch_tags)
        scored.append((s, bm))

    scored = sorted(scored, key=lambda x: x[0], reverse=True)

    top5 = [bm for s, bm in scored if s > 0][:5]
    if not top5:
        # fallback: just first 5 if no overlap (unlikely, but safe)
        top5 = BUSINESS_MODELS[:5]

    st.markdown(f"### Top 5 suggested models for **{selected_arch}**")

    cols = st.columns(2)
    for i, bm in enumerate(top5):
        with cols[i % 2]:
            # CRITICAL: render as HTML, not text
            st.markdown(render_bm_tile(bm), unsafe_allow_html=True)
else:
    st.info("No archetype_tags.json found. Skipping archetype recommendations.")


# -----------------------------
# SECTION 2: Full Library
# -----------------------------
st.markdown("---")
st.markdown("## 2. Browse all 70 business models")

col1, col2 = st.columns([2, 1])

with col1:
    search = st.text_input("Search by name, description, or tag:", "").lower().strip()

with col2:
    all_tags = sorted({t for bm in BUSINESS_MODELS for t in bm.get("tags", [])})
    tag_filter = st.multiselect("Filter by tags:", all_tags)

# Filter logic
filtered = []
for bm in BUSINESS_MODELS:
    block = (
        bm["name"]
        + " "
        + bm.get("description", "")
        + " "
        + " ".join(bm.get("tags", []))
    ).lower()

    if search and search not in block:
        continue

    if tag_filter:
        if not set(tag_filter).issubset(set(bm.get("tags", []))):
            continue

    filtered.append(bm)

st.markdown(f"**{len(filtered)} models shown**")

# 3-column grid for all models
grid_cols = st.columns(3)
for i, bm in enumerate(filtered):
    with grid_cols[i % 3]:
        st.markdown(render_bm_tile(bm), unsafe_allow_html=True)


