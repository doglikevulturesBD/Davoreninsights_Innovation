import streamlit as st
import json
import os

st.set_page_config(layout="wide")

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------
DATA_PATH = "data/business_models.json"

if not os.path.exists(DATA_PATH):
    st.error(f"Could not find {DATA_PATH}. Please upload the file.")
    st.stop()

with open(DATA_PATH, "r", encoding="utf-8") as f:
    BUSINESS_MODELS = json.load(f)


ARCHETYPE_TAGS = {
    "Tech Builder": ["software", "AI", "digital", "developer"],
    "Impact Innovator": ["impact", "green", "sustainability"],
    "Hardware Pioneer": ["hardware", "manufacturing", "IoT"],
    "Platform Creator": ["platform", "community", "ecosystem"],
    "Finance/Business Strategist": ["finance", "B2B", "hybrid"],
}


# ---------------------------------------------------------
# CSS (Beautiful Cards)
# ---------------------------------------------------------
st.markdown("""
<style>

.business-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border: 1px solid #f2f2f2;
}

.business-title {
    font-size: 1.25em;
    font-weight: 600;
    color: #222;
    margin-bottom: 2px;
}

.business-id {
    color: #999;
    font-size: 0.85em;
}

.tag-chip {
    display: inline-block;
    padding: 5px 10px;
    margin: 4px 6px 4px 0;
    border-radius: 8px;
    font-size: 0.75em;
    font-weight: 500;
    color: #222;
    background: #E3F2FD;
}

.metric-row {
    display:flex;
    justify-content: space-between;
    font-size: 0.85em;
    color:#444;
    margin-top: 12px;
    margin-bottom: 4px;
}

.section-title {
    font-weight: 700;
    font-size: 0.9em;
    margin-top: 14px;
    margin-bottom: 6px;
    color: #222;
}

ul.detail-list {
    padding-left: 20px;
    margin-top: 4px;
    margin-bottom: 8px;
    font-size: 0.9em;
    color: #333;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Render Tile (HTML)
# ---------------------------------------------------------
def render_tile(bm):

    # Build tag chips
    tag_html = "".join([
        f"<span class='tag-chip'>{t}</span>"
        for t in bm.get("tags", [])
    ])

    # Build lists
    def list_html(items):
        if not items:
            return ""
        inner = "".join([f"<li>{x}</li>" for x in items])
        return f"<ul class='detail-list'>{inner}</ul>"

    # Main HTML
    html = f"""
    <div class="business-card">

        <div class="business-title">{bm['name']}</div>
        <div class="business-id">{bm['id']}</div>

        <p style="margin-top:10px;color:#444;">
            {bm.get("description","")}
        </p>

        <div style="margin-top:12px;">{tag_html}</div>

        <div class="metric-row">
            <div><strong>Difficulty:</strong> {bm.get('difficulty','-')} / 5</div>
            <div><strong>Capex:</strong> {bm.get('capital_requirement','-')}</div>
        </div>

        <div style="font-size:0.85em;color:#444;">
            <strong>Time to Revenue:</strong> {bm.get('time_to_revenue','-')}
        </div>

        <div class="section-title">Revenue Streams</div>
        {list_html(bm.get("revenue_streams", []))}

        <div class="section-title">Use Cases</div>
        {list_html(bm.get("use_cases", []))}

        <div class="section-title">Examples</div>
        {list_html(bm.get("examples", []))}

        <div class="section-title">Risks</div>
        {list_html(bm.get("risks", []))}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------
# Archetype Selection
# ---------------------------------------------------------
st.title("Business Model Selector")

st.subheader("1. Choose your Innovator Archetype")

archetype = st.selectbox("Select your profile:", list(ARCHETYPE_TAGS.keys()))

if not archetype:
    st.stop()

archetype_tags = ARCHETYPE_TAGS[archetype]


# ---------------------------------------------------------
# Scoring Function
# ---------------------------------------------------------
def score_model(model, tags):
    overlap = len(set(model["tags"]) & set(tags))
    return overlap  # simple & effective


# ---------------------------------------------------------
# Ranking
# ---------------------------------------------------------
st.subheader("2. Top Business Model Recommendations")

scored = [(bm, score_model(bm, archetype_tags)) for bm in BUSINESS_MODELS]
scored.sort(key=lambda x: x[1], reverse=True)
top5 = scored[:5]

st.markdown(f"### Top 5 Models for **{archetype}**")

for bm, score in top5:
    render_tile(bm)


# ---------------------------------------------------------
# Expandable — All Models
# ---------------------------------------------------------
with st.expander("See All 70 Business Models"):
    for bm in BUSINESS_MODELS:
        render_tile(bm)



