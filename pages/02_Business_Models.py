import streamlit as st
import json

# -------------------------------------------------------
# LOAD BUSINESS MODELS JSON
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
# CUSTOM CSS
# -------------------------------------------------------
st.markdown("""
<style>

/* --- Card container --- */
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

/* --- Title --- */
.business-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111;
    margin-bottom: 4px;
}

/* --- ID --- */
.business-id {
    color: #777;
    font-size: 0.85rem;
    margin-bottom: 10px;
}

/* --- Tag chips --- */
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

/* --- Metrics row --- */
.metric-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    margin-top: 8px;
    color: #333;
}

/* --- Section titles --- */
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
# PAGE TITLE
# -------------------------------------------------------
st.title("Business Model Navigator")
st.write("Select an archetype or search through all 70 models.")

# -------------------------------------------------------
# SEARCH BAR
# -------------------------------------------------------
search_term = st.text_input("Search business models", "")

# -------------------------------------------------------
# ARCHETYPE SELECTION
# -------------------------------------------------------
selected_arch = st.selectbox("Choose an archetype", ["-- Select --"] + list(ARCHETYPES.keys()))

filtered_models = BUSINESS_MODELS

# Apply archetype filter
if selected_arch != "-- Select --":
    selected_tags = ARCHETYPES[selected_arch]
    filtered_models = [bm for bm in BUSINESS_MODELS if any(t in bm["tags"] for t in selected_tags)]

# Apply search filter
if search_term.strip():
    term = search_term.lower()
    filtered_models = [
        bm for bm in filtered_models
        if term in bm["name"].lower()
        or term in bm["description"].lower()
        or any(term in t.lower() for t in bm["tags"])
    ]

# -------------------------------------------------------
# BUSINESS MODEL CARD RENDERER
# -------------------------------------------------------
def render_model_card(bm):
    tag_html = "".join([f"<span class='tag-chip'>{tag}</span>" for tag in bm["tags"]])

    card_html = f"""
    <div class="business-card">
        <div class="business-title">{bm['name']}</div>
        <div class="business-id">{bm['id']}</div>

        <p style="color:#444; margin-bottom:10px;">{bm['description']}</p>

        <div>{tag_html}</div>

        <div class="metric-row">
            <div><strong>Difficulty:</strong> {bm['difficulty']} / 5</div>
            <div><strong>Capex:</strong> {bm['capital_requirement']}</div>
        </div>

        <div class="desc-text"><strong>Time to Revenue:</strong> {bm['time_to_revenue']}</div>
    """

    # Expandable sections
    card_html += "</div>"  # close initial card

    st.markdown(card_html, unsafe_allow_html=True)

    with st.expander("Revenue Streams"):
        for item in bm["revenue_streams"]:
            st.write("- " + item)

    with st.expander("Use Cases"):
        for item in bm["use_cases"]:
            st.write("- " + item)

    with st.expander("Example Companies"):
        for item in bm["examples"]:
            st.write("- " + item)

    with st.expander("Risks"):
        for item in bm["risks"]:
            st.write("- " + item)


# -------------------------------------------------------
# DISPLAY MODELS
# -------------------------------------------------------
st.subheader(f"{len(filtered_models)} business models found")

for bm in filtered_models:
    render_model_card(bm)
