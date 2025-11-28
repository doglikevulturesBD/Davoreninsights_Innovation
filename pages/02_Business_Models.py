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
# Archetypes
# --------------------------------------------------
ARCHETYPES = {
    "Digital / Software": ["software", "AI", "platform", "data"],
    "Hardware / Manufacturing": ["hardware", "manufacturing", "infrastructure"],
    "Green / Impact": ["green", "impact", "sustainability"],
    "Finance / Investment": ["finance", "hybrid", "public"],
    "Ecosystem / Services": ["services", "community", "B2B"]
}


# --------------------------------------------------
# CSS — Improved Contrast
# --------------------------------------------------
st.markdown("""
<style>

.business-card {
    background-color: #FFFFFF;
    border-radius: 12px;
    border: 1px solid #D0D0D0;
    padding: 18px;
    margin-bottom: 20px;
    transition: all 0.18s ease-in-out;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}

.business-card:hover {
    border: 1px solid #AAAAAA;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transform: translateY(-2px);
}

.business-title {
    font-size: 1.15em;
    font-weight: 600;
    color: #111;       /* darker title */
    margin-bottom: 2px;
}

.business-id {
    color: #555;        /* improved visibility */
    font-size: 0.85em;
}

.tag-chip {
    background: #DCEBFF;
    padding: 5px 10px;
    border-radius: 8px;
    margin-right: 6px;
    margin-bottom: 6px;
    font-size: 0.75em;
    display: inline-block;
    color: #0A2A55;     /* dark readable blue */
    font-weight: 500;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
    font-size: 0.85em;
    color: #333;        /* higher contrast */
}

.section-title {
    margin-top: 14px;
    font-weight: 600;
    color: #111;        /* dark heading in card */
}

.detail-list li {
    margin-bottom: 6px;
    font-size: 0.92em;
    color: #222;        /* readable */
}

p {
    color: #222 !important;   /* override weak greys */
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Page Title + UI
# --------------------------------------------------
st.title("Business Model Explorer")

st.write("""
Choose an archetype OR search directly.  
These models form the foundation of the *DavorenInsights Innovation Education App*.
""")

selected_arch = st.selectbox(
    "Choose an archetype:",
    ["All"] + list(ARCHETYPES.keys())
)

search_term = st.text_input("Search models…", "")


# --------------------------------------------------
# Filtering Logic
# --------------------------------------------------
filtered = BUSINESS_MODELS

if selected_arch != "All":
    tags = ARCHETYPES[selected_arch]
    filtered = [bm for bm in filtered if any(t in bm["tags"] for t in tags)]

if search_term.strip():
    s = search_term.lower()
    filtered = [
        bm for bm in filtered
        if s in bm["name"].lower()
        or s in bm["description"].lower()
        or any(s in t.lower() for t in bm["tags"])
    ]

st.markdown(f"### Showing **{len(filtered)}** business models")


# --------------------------------------------------
# Render model cards
# --------------------------------------------------
cols = st.columns(2)

for i, bm in enumerate(filtered):

    with cols[i % 2]:
        st.markdown("<div class='business-card'>", unsafe_allow_html=True)

        # Title + ID
        st.markdown(f"""
            <div class="business-title">{bm['name']}</div>
            <div class="business-id">{bm['id']}</div>
        """, unsafe_allow_html=True)

        # Description
        st.markdown(
            f"<p style='margin-top:10px;'>{bm['description']}</p>",
            unsafe_allow_html=True
        )

        # Tags
        tags_html = "".join([f"<span class='tag-chip'>{t}</span>" for t in bm["tags"]])
        st.markdown(f"<div style='margin-top:12px;'>{tags_html}</div>", unsafe_allow_html=True)

        # Metrics
        st.markdown(f"""
        <div class='metric-row'>
            <div><strong>Difficulty:</strong> {bm.get("difficulty", "-")} / 5</div>
            <div><strong>Capex:</strong> {bm.get("capital_requirement", "-")}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f"<div style='font-size:0.85em;color:#333;margin-top:4px;'><strong>Time to Revenue:</strong> {bm['time_to_revenue']}</div>",
            unsafe_allow_html=True
        )

        # Expanders (dark text inside)
        with st.expander("Revenue Streams"):
            st.markdown("\n".join([f"- {x}" for x in bm["revenue_streams"]]))

        with st.expander("Use Cases"):
            st.markdown("\n".join([f"- {x}" for x in bm["use_cases"]]))

        with st.expander("Examples"):
            st.markdown("\n".join([f"- {x}" for x in bm["examples"]]))

        with st.expander("Risks"):
            st.markdown("\n".join([f"- {x}" for x in bm["risks"]]))

        st.markdown("</div>", unsafe_allow_html=True)


