import streamlit as st
import json
import re


# --- Load models ---
with open("data/business_models.json", "r") as f:
    BUSINESS_MODELS = json.load(f)


# --- CSS injected once ---
st.markdown("""
<style>
.business-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 16px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    transition: 0.2s;
}
.business-card:hover {
    box-shadow: 0px 6px 14px rgba(0,0,0,0.12);
}
.business-title {
    font-size: 1.2em;
    font-weight: 600;
    color: #222;
}
.business-id {
    font-size: 0.85em;
    color: #777;
    margin-bottom: 10px;
}
.tag-chip {
    background: #E8F1FF;
    padding: 6px 10px;
    border-radius: 8px;
    margin-right: 6px;
    font-size: 0.75em;
    display: inline-block;
    color: #222;
}
.metric-row {
    display:flex;
    justify-content:space-between;
    margin-top:10px;
    font-size:0.85em;
    color:#444;
}
.desc-text {
    margin-top:8px;
    font-size:0.85em;
    color:#444;
}
.detail-list {
    margin-top:6px;
    padding-left:20px;
    color:#333;
    font-size:0.9em;
}
details {
    margin-top: 10px;
    padding: 8px 0px;
}
details summary {
    cursor: pointer;
    font-weight: 600;
    color: #222;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)


def render_card(bm):

    tags_html = "".join(f"<span class='tag-chip'>{t}</span>" for t in bm["tags"])

    revenue_li = "".join(f"<li>{x}</li>" for x in bm["revenue_streams"])
    use_li = "".join(f"<li>{x}</li>" for x in bm["use_cases"])
    example_li = "".join(f"<li>{x}</li>" for x in bm["examples"])
    risk_li = "".join(f"<li>{x}</li>" for x in bm["risks"])

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

        <details>
            <summary>Revenue Streams</summary>
            <ul class="detail-list">{revenue_li}</ul>
        </details>

        <details>
            <summary>Use Cases</summary>
            <ul class="detail-list">{use_li}</ul>
        </details>

        <details>
            <summary>Examples</summary>
            <ul class="detail-list">{example_li}</ul>
        </details>

        <details>
            <summary>Risks</summary>
            <ul class="detail-list">{risk_li}</ul>
        </details>

    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


# --- Render all models for testing ---
for bm in BUSINESS_MODELS[:10]:     # test first 10
    render_card(bm)

