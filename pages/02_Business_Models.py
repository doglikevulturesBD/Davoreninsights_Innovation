import streamlit as st
import json
import re


def strip_html(text):
    return re.sub(r"<.*?>", "", text)


with open("data/business_models.json", "r") as f:
    BUSINESS_MODELS = json.load(f)


def render_card(bm):

    # Clean data if HTML sneaked into JSON
    desc = strip_html(bm["description"])
    revenue = [strip_html(x) for x in bm["revenue_streams"]]
    use_cases = [strip_html(x) for x in bm["use_cases"]]
    examples = [strip_html(x) for x in bm["examples"]]
    risks = [strip_html(x) for x in bm["risks"]]

    tags_html = "".join(f"<span class='tag-chip'>{t}</span>" for t in bm["tags"])

    html = f"""
    <div class="business-card">
        <div class="business-title">{bm['name']}</div>
        <div class="business-id">{bm['id']}</div>

        <p style='color:#444; margin-bottom:10px;'>{desc}</p>

        <div>{tags_html}</div>

        <div class="metric-row">
            <div><strong>Difficulty:</strong> {bm['difficulty']} / 5</div>
            <div><strong>Capex:</strong> {bm['capital_requirement']}</div>
        </div>

        <div class="desc-text"><strong>Time to Revenue:</strong> {bm['time_to_revenue']}</div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

    with st.expander("Revenue Streams"):
        for i in revenue:
            st.write("- " + i)

    with st.expander("Use Cases"):
        for i in use_cases:
            st.write("- " + i)

    with st.expander("Examples"):
        for i in examples:
            st.write("- " + i)

    with st.expander("Risks"):
        for i in risks:
            st.write("- " + i)


