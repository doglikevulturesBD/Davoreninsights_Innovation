import streamlit as st
import json
import os

st.set_page_config(page_title="Business Models", layout="wide")

st.title("Business Model Selector — Education View")
st.write(
    "Pick an innovator archetype to see the top-fitting business models. "
    "You can also search or browse the full library of 70 models."
)

# -----------------------------
# Load data
# -----------------------------
BM_PATH = "data/business_models.json"
ARCH_PATH = "data/archetype_tags.json"

with open(BM_PATH, "r", encoding="utf-8") as f:
    BUSINESS_MODELS = json.load(f)

with open(ARCH_PATH, "r", encoding="utf-8") as f:
    ARCHETYPE_TAGS = json.load(f)


# -----------------------------
# Scoring (simple overlap)
# -----------------------------
def score_for_archetype(bm, tags):
    return len(set(bm.get("tags", [])) & set(tags))


# -----------------------------
# Tile Renderer (no HTML)
# -----------------------------
def render_tile(bm):
    st.subheader(f"{bm['name']}  — `{bm['id']}`")
    st.markdown(bm.get("description", ""))

    # Tags row
    tags = bm.get("tags", [])
    if tags:
        st.markdown("**Tags:** " + ", ".join(f"`{t}`" for t in tags))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Difficulty:** {bm.get('difficulty', '-')} / 5")
    with col2:
        st.markdown(f"**Capex:** {bm.get('capital_requirement', '-')}")
    with col3:
        st.markdown(f"**Time to Revenue:** {bm.get('time_to_revenue', '-')}")

    # Lists
    def bullet_list(title, items):
        st.markdown(f"**{title}:**")
        for it in items:
            st.markdown(f"- {it}")

    bullet_list("Revenue Streams", bm.get("revenue_streams", []))
    bullet_list("Use Cases", bm.get("use_cases", []))
    bullet_list("Examples", bm.get("examples", []))
    bullet_list("Risks", bm.get("risks", []))

    st.markdown("---")


# -----------------------------
# UI — Archetype
# -----------------------------
st.markdown("### 1. Choose your innovator archetype")

archetypes = list(ARCHETYPE_TAGS.keys())
selected_arch = st.radio("Select your archetype:", archetypes)
arch_tags = ARCHETYPE_TAGS[selected_arch]

st.info(f"You selected **{selected_arch}** — matching tags: {', '.join(arch_tags)}")

# -----------------------------
# Generate Top 5
# -----------------------------
generate = st.button("Generate Top 5 Business Models")

top5_models = []
if generate:
    scored = [(score_for_archetype(bm, arch_tags), bm) for bm in BUSINESS_MODELS]
    scored.sort(key=lambda x: (-x[0], x[1]['name']))

    # Top 5 with some overlap
    top5_models = [bm for score, bm in scored if score > 0][:5]
    if not top5_models:
        top5_models = [bm for score, bm in scored[:5]]

    st.markdown("### 2. Recommended Top 5 Models")
    for bm in top5_models:
        render_tile(bm)


# -----------------------------
# Search + Show All Models
# -----------------------------
st.markdown("### 3. Explore All Business Models")

with st.expander("Search & Browse All Models"):
    search_query = st.text_input("Search by name or tag:")
    show_all = st.checkbox("Show all business models", value=False)

    filtered_models = BUSINESS_MODELS

    # Apply search filter
    if search_query:
        q = search_query.lower()
        def matches(bm):
            name_match = q in bm['name'].lower()
            desc_match = q in bm.get("description", "").lower()
            tag_match = any(q in t.lower() for t in bm.get("tags", []))
            return name_match or desc_match or tag_match
        filtered_models = [bm for bm in BUSINESS_MODELS if matches(bm)]

    if show_all or search_query:
        st.markdown(f"**{len(filtered_models)} models found**")
        for bm in filtered_models:
            render_tile(bm)



