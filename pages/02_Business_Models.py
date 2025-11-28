import streamlit as st
import json
import os

st.set_page_config(page_title="Business Models", layout="wide")

# --------------------------------------------------
# Load BM JSON
# --------------------------------------------------
DATA_PATH = "data/business_models.json"

if not os.path.exists(DATA_PATH):
    st.error("business_models.json missing in /data folder.")
    st.stop()

with open(DATA_PATH, "r") as f:
    BUSINESS_MODELS = json.load(f)


# --------------------------------------------------
# Archetype definitions
# --------------------------------------------------
ARCHETYPES = {
    "Digital / Software": ["software", "AI", "platform", "data"],
    "Hardware / Manufacturing": ["hardware", "manufacturing", "infrastructure"],
    "Green / Impact": ["green", "impact", "sustainability"],
    "Finance / Investment": ["finance", "hybrid", "public"],
    "Ecosystem / Services": ["services", "community", "B2B"]
}


# --------------------------------------------------
# CSS for tiles + hover + spacing
# --------------------------------------------------
st.markdown("""
<style>

.business-card {
    background-color: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #E0E0E0;
    padding: 18px;
    margin-bottom: 20px;
    transition: all 0.18s ease-in-out;
    box-shadow: 0 2px 4px rgba(0,0,0,0.06);
}

.business-card:hover {
    border: 1px solid #BBBBBB;
    box-shadow: 0 4px 10px rgba(0,0,0,0.12);
    transform: translateY(-2px);
}

.tag-chip {
    background: #E8F4FF;
    padding: 5px 10px;
    border-radius: 8px;
    margin-right: 6px;
    margin-bottom: 6px;
    font-size: 0.75em;
    display: inline-block;
    color: #0A3A75;
}

.business-title {
    font-size: 1.15em;
    font-weight: 600;
    color: #222;
    margin-bottom: 2px;
}

.business-id {
    color: #777;
    font-size: 0.85em;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
    font-size: 0.85em;
    color: #444;
}

.section-title {
    margin-top: 14px;
    font-weight: 600;
    color: #222;
}

.detail-list li {
    margin-bottom: 4px;
    font-size: 0.9em;
    color: #333;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Title + Selectors
# --------------------------------------------------
st.title("Business Model Explorer")

st.write("""
Choose an archetype OR search directly.  
These models form the foundation of the *DavorenInsights Innovation Education App*.
""")

selected_arch = st.selectbox(
    "Choose an archetype to explore:",
    ["All"] + list(ARCHETYPES.keys())
)

search_term = st.text_input("Search business models", "")

# --------------------------------------------------
# Filter logic
# --------------------------------------------------
filtered_models = BUSINESS_MODELS

if selected_arch != "All":
    tags = ARCHETYPES[selected_arch]
    filtered_models = [bm for bm in filtered_models if any(t in bm["tags"] for t in tags)]

if search_term.strip():
    search_term = search_term.lower()
    filtered_models = [
        bm for bm in filtered_models
        if search_term in bm["name"].lower() 
        or search_term in bm["description"].lower()
        or any(search_term in t.lower() for t in bm["tags"])
    ]

st.markdown(f"### Showing **{len(filtered_models)}** models")

cols = st.columns(2)

# --------------------------------------------------
# Render cards
# --------------------------------------------------
for i, bm in enumerate(filtered_models):

    with cols[i % 2]:
        # Open card wrapper
        st.markdown("<div class='business-card'>", unsafe_allow_html=True)

        # Title + ID
        st.markdown(f"""
            <div class="business-title">{bm['name']}</div>
            <div class="business-id">{bm['id']}</div>
        """, unsafe_allow_html=True)

        # Description
        st.markdown(
            f"<p style='margin-top:10px;color:#444;'>{bm['description']}</p>",
            unsafe_allow_html=True
        )

        # Tags
        tag_block = "".join([f"<span class='tag-chip'>{t}</span>" for t in bm["tags"]])
        st.markdown(f"<div style='margin-top:12px;'>{tag_block}</div>", unsafe_allow_html=True)

        # Metrics
        st.markdown(f"""
        <div class='metric-row'>
            <div><strong>Difficulty:</strong> {bm.get("difficulty", "-")} / 5</div>
            <div><strong>Capex:</strong> {bm.get("capital_requirement", "-")}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f"<div style='font-size:0.85em;color:#444;'><strong>Time to Revenue:</strong> {bm['time_to_revenue']}</div>",
            unsafe_allow_html=True
        )

        # Expanders
        with st.expander("Revenue Streams"):
            st.markdown("\n".join([f"- {x}" for x in bm["revenue_streams"]]))

        with st.expander("Use Cases"):
            st.markdown("\n".join([f"- {x}" for x in bm["use_cases"]]))

        with st.expander("Examples"):
            st.markdown("\n".join([f"- {x}" for x in bm["examples"]]))

        with st.expander("Risks"):
            st.markdown("\n".join([f"- {x}" for x in bm["risks"]]))

        # Close card wrapper
        st.markdown("</div>", unsafe_allow_html=True)


