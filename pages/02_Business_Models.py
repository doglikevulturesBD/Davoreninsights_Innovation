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

# ---------------------------
# UI Header
# ---------------------------
st.title("Business Model Explorer")

st.write("Select an archetype below to explore the most relevant business models:")

# ---------------------------
# Archetype Selection
# ---------------------------
selected_arch = st.segmented_control(
    "Choose a Business Model Archetype",
    list(ARCHETYPES.keys()) + ["Show All Models"]
)

st.divider()

# ---------------------------
# Filter Models Based on Archetype
# ---------------------------
if selected_arch == "Show All Models":
    filtered = MODELS
else:
    tags = ARCHETYPES[selected_arch]
    filtered = [m for m in MODELS if any(t in m["tags"] for t in tags)]

# ---------------------------
# Search Bar
# ---------------------------
query = st.text_input("Search models:", "")

if query:
    filtered = [m for m in filtered if query.lower() in m["name"].lower()]

# ---------------------------
# 2-Column Layout Rendering
# ---------------------------
cols = st.columns(2)

for index, bm in enumerate(filtered):
    with cols[index % 2].container(border=True, padding=15):

        # Header
        st.subheader(bm["name"])
        st.caption(bm["id"])

        # Description
        st.write(bm["description"])

        # Tags
        tag_cols = st.columns(len(bm["tags"]))
        for i, tag in enumerate(bm["tags"]):
            tag_cols[i].markdown(f"🟦 **{tag}**")

        # Metrics Row
        col1, col2 = st.columns(2)
        col1.write(f"**Difficulty:** {bm['difficulty']} / 5")
        col2.write(f"**Capex:** {bm['capital_requirement']}")

        # Time to revenue
        st.write(f"**Time to revenue:** {bm['time_to_revenue']}")

        # Revenue Streams
        with st.expander("Revenue Streams"):
            st.write("\n".join([f"- {x}" for x in bm["revenue_streams"]]))

        # Use Cases
        with st.expander("Use Cases"):
            st.write("\n".join([f"- {x}" for x in bm["use_cases"]]))

        # Examples
        with st.expander("Examples"):
            st.write("\n".join([f"- {x}" for x in bm["examples"]]))

        # Risks
        with st.expander("Risks"):
            st.write("\n".join([f"- {x}" for x in bm["risks"]]))


