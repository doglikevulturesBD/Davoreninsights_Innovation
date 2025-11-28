import streamlit as st
import json
import os

st.set_page_config(page_title="Business Models", layout="wide")

# ---------------------------
# Load Data
# ---------------------------
DATA_PATH = os.path.join("data", "business_models.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    MODELS = json.load(f)

# ---------------------------
# Archetype Definitions
# ---------------------------
ARCHETYPES = {
    "Digital & Software": ["software", "digital", "AI", "developer", "data", "recurring"],
    "Hardware & Manufacturing": ["hardware", "manufacturing", "IoT", "high_capex", "OEM"],
    "Services & Consulting": ["services", "operations", "learning"],
    "Platform & Ecosystem": ["platform", "ecosystem", "community", "marketplace", "crowd"],
    "Impact & Sustainability": ["impact", "green", "carbon", "local", "sustainability"],
}

ARCTYPE_OPTIONS = list(ARCHETYPES.keys()) + ["Show All Models"]

# ---------------------------
# UI Header
# ---------------------------
st.title("Business Model Explorer")
st.write("Select an archetype below to explore models most suited to your innovation strategy.")

# ---------------------------
# Archetype Selection Widget
# ---------------------------
selected_arch = st.segmented_control(
    "Choose a Business Model Archetype",
    options=ARCTYPE_OPTIONS,
    default=None
)

st.divider()

# ---------------------------
# Filter Logic (Safe)
# ---------------------------
if not selected_arch:
    st.info("Please choose an archetype above to continue.")
    st.stop()

if selected_arch == "Show All Models":
    filtered = MODELS
else:
    # SAFE ACCESS → no KeyError possible
    tags = ARCHETYPES.get(selected_arch, [])
    filtered = [m for m in MODELS if any(t in m["tags"] for t in tags)]

# ---------------------------
# Search Bar
# ---------------------------
query = st.text_input("Search models:", "")

if query:
    filtered = [m for m in filtered if query.lower() in m["name"].lower()]

# ---------------------------
# Render Tiles in 2 Columns
# ---------------------------
cols = st.columns(2)

for index, bm in enumerate(filtered):
    with cols[index % 2].container(border=True, padding=15):

        st.subheader(bm["name"])
        st.caption(bm["id"])

        st.write(bm["description"])

        # Tags as pills
        tag_cols = st.columns(min(len(bm["tags"]), 4))
        for i, tag in enumerate(bm["tags"]):
            tag_cols[i % 4].markdown(f"🟦 **{tag}**")

        col1, col2 = st.columns(2)
        col1.write(f"**Difficulty:** {bm['difficulty']} / 5")
        col2.write(f"**Capex:** {bm['capital_requirement']}")

        st.write(f"**Time to revenue:** {bm['time_to_revenue']}")

        # Rich details
        with st.expander("Revenue Streams"):
            st.markdown("\n".join([f"- {x}" for x in bm["revenue_streams"]]))

        with st.expander("Use Cases"):
            st.markdown("\n".join([f"- {x}" for x in bm["use_cases"]]))

        with st.expander("Examples"):
            st.markdown("\n".join([f"- {x}" for x in bm["examples"]]))

        with st.expander("Risks"):
            st.markdown("\n".join([f"- {x}" for x in bm["risks"]]))


