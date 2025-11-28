import streamlit as st
import json

# -------------------------------------------------------
# LOAD CLEAN JSON (TEXT ONLY, NO HTML)
# -------------------------------------------------------
with open("data/business_models.json", "r") as f:
    BUSINESS_MODELS = json.load(f)

# -------------------------------------------------------
# ARCHETYPES
# -------------------------------------------------------
ARCHETYPES = {
    "Digital / Software": ["software", "digital", "AI", "cloud"],
    "Platform / Ecosystem": ["platform", "community", "ecosystem", "transaction"],
    "Hardware / Manufacturing": ["hardware", "manufacturing", "IoT", "high_capex"],
    "Services / Consulting": ["services", "B2B", "operations", "learning"],
    "Impact / Climate / Green": ["impact", "green", "sustainability", "finance"]
}

# -------------------------------------------------------
# CSS STYLES
# -------------------------------------------------------
st.markdown("""
<style>

.business-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 25px;
    border: 1px solid #e6e6e6;
    transition: all 0.2s ease;
}
.business-card:hover {
    border-color: #4A90E2;
    box-shadow: 0 0 12px rgba(0,0,0,0.08);
    transform: translateY(-3px);
}

.business-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111;
    margin-bottom: 4px;
}
.business-id {
    color: #777;
    font-size: 0.85rem;
    margin-bottom: 10px;
}

.tag-chip {
    background: #e8f0fe;
    color: #1a237e;
    padding: 5px 10px;
    border-radius: 12px;
    margin-right: 6px;
    margin-bottom: 6px;
    display: inline-block;
    font-size: 0.75rem;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    margin-top: 8px;
    color: #333;
}

.section-label {
    font-weight: 600;
    color: #111;
    margin-top: 12px;
    margin-bottom: 4px;
}

.desc-text {
    color: #333;
    font-size: 0.9rem;
    margin-top: 6px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# TITLE
# -------------------------------------------------------
st.title("Business Model Navigator")

search_term = st.text_input("Search business models", "")

selected_arch = st.selectbox("Choose an archetype", ["-- Select --"] + list(ARCHETYPES.keys()))

filtered = BUSINESS_MODELS

# ARCHETYPE FILTER
if selected_arch != "-- Select --":
    t = ARCHETYPES[selected_arch]
    filtered = [b for b in filtered if any(tag in b["tags"] for tag in t)]

# SEARCH FILTER
if search_term.strip():
    s = search_term.lower()
    filtered = [
        b for b in filtered
        if s in b["name"].lower()
        or s in b["description"].lower()
        or any(s in t.lower() for t in b["tags"])
    ]

# -------------------------------------------------------
# SAFE HTML CARD RENDERER (NO HTML FROM JSON)
# -------------------------------------------------------
def render_card(bm):
    # tag chips
    tags_html = "".join(f"<span class='tag-chip'>{t}</span>" for t in bm["tags"])

    # build the HTML card — ALL HTML generated here (safe)
    html = f"""
    <div class="business-card">
        <div class="business-title">{bm['name']}</div>
        <div class="business-id">{bm['id']}</div>

        <p style="color:#444; margin-bottom:10px;">{bm['description']}</p>

        <div>{tags_html}</div>

        <div class="metric-row">
            <div><strong>Difficulty:</strong> {bm['difficulty']} / 5</div>
            <div><strong>Capex:</strong> {bm['capital_requirement']}</div>
        </div>

        <div class="desc-text"><strong>Time to Revenue:</strong> {bm['time_to_revenue']}</div>
    </div>
    """

    # render card
    st.markdown(html, unsafe_allow_html=True)

    # expanders
    with st.expander("Revenue Streams"):
        for i in bm["revenue_streams"]:
            st.write("- " + i)

    with st.expander("Use Cases"):
        for i in bm["use_cases"]:
            st.write("- " + i)

    with st.expander("Examples"):
        for i in bm["examples"]:
            st.write("- " + i)

    with st.expander("Risks"):
        for i in bm["risks"]:
            st.write("- " + i)


# -------------------------------------------------------
# DISPLAY MODELS
# -------------------------------------------------------
st.subheader(f"{len(filtered)} business models found")

for model in filtered:
    render_card(model)

