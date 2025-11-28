import streamlit as st
import json

st.set_page_config(layout="wide")

# ------------------------------------------------------
# Load Business Models
# ------------------------------------------------------
with open("data/business_models.json", "r") as f:
    BUSINESS_MODELS = json.load(f)

# ------------------------------------------------------
# Archetypes
# ------------------------------------------------------
ARCHETYPES = {
    "Digital SaaS / AI Tools": ["software", "AI", "digital", "recurring"],
    "Platforms & Ecosystems": ["platform", "community", "ecosystem", "transaction"],
    "Hardware & Energy Systems": ["hardware", "IoT", "infrastructure", "high_capex"],
    "Finance & Climate Models": ["finance", "impact", "green", "hybrid"],
    "Social / Community / Impact": ["local", "cooperative", "impact", "community"]
}

# ------------------------------------------------------
# CSS Styles (modern, clean, high contrast)
# ------------------------------------------------------
st.markdown("""
<style>

.business-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 16px;
    border: 1px solid #e6e6e6;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.business-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.18);
}

.business-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #222;
    margin-bottom: 4px;
}

.business-id {
    font-size: 0.80rem;
    color: #777;
    margin-bottom: 10px;
}

.desc-text {
    font-size: 0.90rem;
    color: #333;
    margin-bottom: 12px;
}

.tag-chip {
    background: #EEF2FF;
    border-radius: 8px;
    padding: 4px 10px;
    margin-right: 6px;
    display: inline-block;
    font-size: 0.75rem;
    color: #222;
    border: 1px solid #ddd;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    color: #333;
    font-size: 0.85rem;
    margin-top: 12px;
    margin-bottom: 6px;
}

.section-title {
    font-weight: 700;
    margin-top: 12px;
    font-size: 0.9rem;
    color: #222;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# Title
# ------------------------------------------------------
st.title("Business Model Explorer 🚀")
st.write("Select an archetype to view relevant business models.")

# ------------------------------------------------------
# Step 1 — Select Archetype
# ------------------------------------------------------
selected_arch = st.selectbox("Choose Business Model Archetype:", [""] + list(ARCHETYPES.keys()))

if not selected_arch:
    st.info("Please select an archetype above to continue.")
    st.stop()

tags_to_filter = ARCHETYPES[selected_arch]

# ------------------------------------------------------
# Step 2 — Filter Models
# ------------------------------------------------------
filtered = [bm for bm in BUSINESS_MODELS if any(t in bm["tags"] for t in tags_to_filter)]

st.subheader(f"Recommended Models for: **{selected_arch}**")
st.caption(f"{len(filtered)} matching models found.")

cols = st.columns(2)

# ------------------------------------------------------
# Step 3 — Display cards
# ------------------------------------------------------
for i, bm in enumerate(filtered):

    card_html = f"""
    <div class='business-card'>
        <div class='business-title'>{bm["name"]}</div>
        <div class='business-id'>{bm["id"]}</div>
        <div class='desc-text'>{bm["description"]}</div>

        <div style="margin-bottom:8px;">
            {''.join([f"<span class='tag-chip'>{t}</span>" for t in bm["tags"]])}
        </div>

        <div class='metric-row'>
            <div><strong>Difficulty:</strong> {bm["difficulty"]} / 5</div>
            <div><strong>Capex:</strong> {bm["capital_requirement"]}</div>
        </div>

        <div class='desc-text'>
            <strong>Time to Revenue:</strong> {bm["time_to_revenue"]}
        </div>
    </div>
    """

    with cols[i % 2]:
        st.markdown(card_html, unsafe_allow_html=True)

        with st.expander("Revenue Streams"):
            st.markdown("\n".join([f"- {x}" for x in bm["revenue_streams"]]))

        with st.expander("Use Cases"):
            st.markdown("\n".join([f"- {x}" for x in bm["use_cases"]]))

        with st.expander("Examples"):
            st.markdown("\n".join([f"- {x}" for x in bm["examples"]]))

        with st.expander("Risks"):
            st.markdown("\n".join([f"- {x}" for x in bm["risks"]]))


