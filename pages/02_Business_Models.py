import streamlit as st
import json

st.set_page_config(layout="wide")

# -----------------------------
# Load Business Model JSON
# -----------------------------
with open("data/business_models.json", "r") as f:
    BUSINESS_MODELS = json.load(f)

# -----------------------------
# Nice colour choices
# -----------------------------
CARD_BG = "#ffffff"
TAG_BG1 = "#E3F2FD"
TAG_BG2 = "#E8F5E9"
TAG_BG3 = "#EFEFEF"


# -----------------------------
# Render Business Model Tile
# -----------------------------
def render_tile(bm):
    tags_html = ""
    alternating = [TAG_BG1, TAG_BG2, TAG_BG3]
    for i, tag in enumerate(bm["tags"]):
        bg = alternating[i % len(alternating)]
        tags_html += f"""
        <span style="
            background:{bg};
            padding:6px 10px;
            border-radius:8px;
            margin-right:6px;
            font-size:0.8em;
            display:inline-block;
            color:#111;
        ">{tag}</span>
        """

    # Create UL lists
    def make_list(items):
        return "<ul style='margin-top:6px;margin-bottom:12px;padding-left:22px;'>" + \
               "".join([f"<li style='margin-bottom:4px;color:#333;font-size:0.9em;'>{x}</li>"
                        for x in items]) + "</ul>"

    revenue_list = make_list(bm["revenue_streams"])
    use_list = make_list(bm["use_cases"])
    example_list = make_list(bm["examples"])
    risk_list = make_list(bm["risks"])

    html = f"""
    <div style="
        background:{CARD_BG};
        padding:20px;
        border-radius:14px;
        border:1px solid #DDD;
        box-shadow:0 2px 10px rgba(0,0,0,0.06);
        margin-bottom:24px;
    ">
        <h3 style="margin-bottom:4px;color:#111;">{bm['name']}</h3>
        <span style="color:#666;font-size:0.85em;">{bm['id']}</span>

        <p style="margin-top:12px;color:#333;">
            {bm['description']}
        </p>

        <div style="margin:12px 0;">
            {tags_html}
        </div>

        <div style="
            display:flex;
            justify-content:space-between;
            font-size:0.85em;
            color:#444;
            margin-top:10px;
        ">
            <div><strong>Difficulty:</strong> {bm['difficulty']} / 5</div>
            <div><strong>Capex:</strong> {bm['capital_requirement']}</div>
        </div>

        <div style="font-size:0.85em;color:#444;margin-top:8px;">
            <strong>Time to Revenue:</strong> {bm['time_to_revenue']}
        </div>

        <hr style="margin:16px 0;border:0;border-top:1px solid #EEE;">

        <div style="margin-top:8px;">
            <strong style="color:#111;">Revenue Streams</strong>
            {revenue_list}
        </div>

        <div style="margin-top:8px;">
            <strong style="color:#111;">Use Cases</strong>
            {use_list}
        </div>

        <div style="margin-top:8px;">
            <strong style="color:#111;">Examples</strong>
            {example_list}
        </div>

        <div style="margin-top:8px;">
            <strong style="color:#111;">Risks</strong>
            {risk_list}
        </div>
    </div>
    """
    return html


# -----------------------------
# UI Layout
# -----------------------------
st.title("Business Model Library")
st.write("Explore detailed business models with examples, revenue streams, risks, and tags.")

# -----------------------------
# Archetype or Filters (basic for now)
# -----------------------------
tags_available = sorted(list({tag for bm in BUSINESS_MODELS for tag in bm["tags"]}))
selected_tags = st.multiselect("Filter by tags:", tags_available)

difficulty_filter = st.slider("Max Difficulty", 1, 5, 5)


# -----------------------------
# Filter models
# -----------------------------
filtered = []
for bm in BUSINESS_MODELS:
    if bm["difficulty"] <= difficulty_filter:
        if selected_tags:
            if not any(t in bm["tags"] for t in selected_tags):
                continue
        filtered.append(bm)

st.subheader(f"{len(filtered)} models found")

# -----------------------------
# Display tiles
# -----------------------------
for bm in filtered:
    st.markdown(render_tile(bm), unsafe_allow_html=True)


