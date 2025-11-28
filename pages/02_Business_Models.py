import streamlit as st
import json
import os

st.set_page_config(page_title="Business Models", layout="wide")

# --------------------------------------------------
# Load JSON
# --------------------------------------------------
DATA_PATH = "data/business_models.json"

if not os.path.exists(DATA_PATH):
    st.error("JSON file missing.")
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
# CSS (theme-aware, beautiful)
# --------------------------------------------------
st.markdown("""
<style>

/* Make cards theme-aware */
:root {
    --card-bg-light: #FAFAFA;
    --card-bg-dark: #1E1E1E;
    --text-light: #111;
    --text-dark: #EEE;
    --subtext-light: #333;
    --subtext-dark: #CCC;
}

/* Use Streamlit's theme detection */
html[data-theme="light"] {
    --card-bg: var(--card-bg-light);
    --text-primary: var(--text-light);
    --text-secondary: var(--subtext-light);
}

html[data-theme="dark"] {
    --card-bg: var(--card-bg-dark);
    --text-primary: var(--text-dark);
    --text-secondary: var(--subtext-dark);
}

.business-card {
    background-color: var(--card-bg);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 22px;
    border: 1px solid rgba(200,200,200,0.18);
    transition: all 0.2s ease-in-out;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

.business-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.18);
    border-color: rgba(180,180,180,0.4);
}

.business-title {
    font-size: 1.2em;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.business-id {
    color: var(--text-secondary);
    font-size: 0.8em;
    margin-bottom: 12px;
}

.desc-text {
    color: var(--text-secondary);
    font-size: 0.92em;
}

.tag-chip {
    background: rgba(120,160,255,0.15);
    padding: 6px 12px;
    border-radius: 999px;
    margin-right: 8px;
    margin-bottom: 6px;
    font-size: 0.75em;
    display: inline-block;
    color: var(--text-primary);
    border: 1px solid rgba(120,120,255,0.25);
}

.metric-row {
    display: flex;
    justify-content: space-between;
    margin-top: 12px;
    font-size: 0.85em;
    color: var(--text-secondary);
}

.section-title {
    margin-top: 18px;
    font-weight: 600;
    color: var(--text-primary);
}

.detail-list li {
    margin-bottom: 6px;
    font-size: 0.92em;
    color: var(--text-secondary);
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# UI controls
# --------------------------------------------------
st.title("Business Model Explorer")

selected_arch = st.selectbox("Choose Archetype:", ["All"] + list(ARCHETYPES.keys()))
query = st.text_input("Search Models...")


# --------------------------------------------------
# Filtering
# --------------------------------------------------
filtered = BUSINESS_MODELS

if selected_arch != "All":
    tags = ARCHETYPES[selected_arch]
    filtered = [m for m in filtered if any(t in m["tags"] for t in tags)]

if query.strip():
    q = query.lower()
    filtered = [
        m for m in filtered
        if q in m["name"].lower()
        or q in m["description"].lower()
        or any(q in t.lower() for t in m["tags"])
    ]

st.markdown(f"### Showing **{len(filtered)}** models")


# --------------------------------------------------
# Display cards
# --------------------------------------------------
cols = st.columns(2)

for i, bm in enumerate(filtered):
    with cols[i % 2]:
        st.markdown("<div class='business-card'>", unsafe_allow_html=True)

        # Title + ID
        st.markdown(
            f"""
            <div class='business-title'>{bm["name"]}</div>
            <div class='business-id'>{bm["id"]}</div>
            """,
            unsafe_allow_html=True
        )

        # Description
        st.markdown(
            f"<div class='desc-text'>{bm['description']}</div>",
            unsafe_allow_html=True
        )

        # Tags
        tags_html = "".join([f"<span class='tag-chip'>{t}</span>" for t in bm["tags"]])
        st.markdown(f"<div style='margin-top:12px;'>{tags_html}</div>", unsafe_allow_html=True)

        # Metrics
        st.markdown(
            f"""
            <div class='metric-row'>
                <div><strong>Difficulty:</strong> {bm.get("difficulty","-")} / 5</div>
                <div><strong>Capex:</strong> {bm.get("capital_requirement","-")}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div class='desc-text'><strong>Time to Revenue:</strong> {bm['time_to_revenue']}</div>",
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

        st.markdown("</div>", unsafe_allow_html=True)

