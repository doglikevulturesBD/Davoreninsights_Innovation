import streamlit as st
import json
import os

st.set_page_config(page_title="Business Models", layout="wide")

st.title("Business Model Selector — Education View")
st.write(
    "Pick an innovator archetype, and we’ll show the top 5 fitting business models "
    "with teaching-ready detail."
)

# -----------------------------
# Load data
# -----------------------------
BM_PATH = "data/business_models.json"
ARCH_PATH = "data/archetype_tags.json"

if not os.path.exists(BM_PATH):
    st.error(f"Could not find {BM_PATH}")
    st.stop()

with open(BM_PATH, "r", encoding="utf-8") as f:
    BUSINESS_MODELS = json.load(f)

if not os.path.exists(ARCH_PATH):
    st.error(f"Could not find {ARCH_PATH} (archetype tags).")
    st.stop()

with open(ARCH_PATH, "r", encoding="utf-8") as f:
    ARCHETYPE_TAGS = json.load(f)


# -----------------------------
# Simple scoring: tag overlap only
# -----------------------------
def score_for_archetype(bm, archetype_tags):
    """Simple score = number of overlapping tags with the archetype."""
    return len(set(bm.get("tags", [])) & set(archetype_tags))


# -----------------------------
# Pretty bullet list helper
# -----------------------------
def render_list(title, items):
    if not items:
        st.markdown(f"**{title}:** —")
        return
    st.markdown(f"**{title}:**")
    for item in items:
        st.markdown(f"- {item}")


# -----------------------------
# UI Step 1: Choose archetype
# -----------------------------
st.markdown("### 1. Choose your innovator archetype")

archetype_names = list(ARCHETYPE_TAGS.keys())
selected_arch = st.radio(
    "Select the profile that best matches you:",
    archetype_names,
    index=0,
)

archetype_tags = ARCHETYPE_TAGS[selected_arch]

st.info(f"You selected **{selected_arch}**. Matching tags: {', '.join(archetype_tags)}")

# -----------------------------
# Button: generate top 5
# -----------------------------
if st.button("Generate Top 5 Business Models"):
    # Score and rank
    scored = []
    for bm in BUSINESS_MODELS:
        s = score_for_archetype(bm, archetype_tags)
        scored.append((s, bm))

    # Sort by score (highest first), then by name for stability
    scored.sort(key=lambda x: (-x[0], x[1]["name"]))

    # Take top 5 with some overlap; if no scores > 0, just fallback to first 5
    top5 = [bm for s, bm in scored if s > 0][:5]
    if not top5:
        top5 = [bm for _, bm in scored[:5]]

    st.markdown("### 2. Recommended Top 5 Models")
    st.caption("These are ranked by how many strategic tags they share with your archetype.")

    for idx, bm in enumerate(top5, start=1):
        with st.container():
            st.markdown(f"#### {idx}. {bm['name']}  \n`{bm['id']}`")
            st.markdown(bm.get("description", ""))

            # Tags row
            tags = bm.get("tags", [])
            if tags:
                st.markdown(
                    "**Tags:** " + ", ".join(f"`{t}`" for t in tags)
                )

            # Quick stats row
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Difficulty:** {bm.get('difficulty', '-')} / 5")
            with col2:
                st.markdown(f"**Capex:** {bm.get('capital_requirement', '-')}")
            with col3:
                st.markdown(f"**Time to revenue:** {bm.get('time_to_revenue', '-')}")

            # Teaching sections
            render_list("Revenue streams", bm.get("revenue_streams", []))
            render_list("Use cases", bm.get("use_cases", []))
            render_list("Examples", bm.get("examples", []))
            render_list("Risks", bm.get("risks", []))

            st.markdown("---")
else:
    st.markdown("### 2. Recommended Top 5 Models")
    st.caption("Click **Generate Top 5 Business Models** to see your personalised suggestions.")



