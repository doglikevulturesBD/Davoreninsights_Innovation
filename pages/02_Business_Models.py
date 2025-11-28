import streamlit as st
import json
import os

st.set_page_config(page_title="Business Models", layout="wide")

st.title("Business Model Library")
st.write("Explore 70 commercialisation archetypes with teaching-ready detail.")

# -----------------------------
# Load JSON
# -----------------------------
DATA_PATH = "data/business_models.json"

if not os.path.exists(DATA_PATH):
    st.error(f"❌ Could not find {DATA_PATH}")
    st.stop()

with open(DATA_PATH, "r", encoding="utf-8") as f:
    models = json.load(f)


# -----------------------------
# HTML TILE RENDERER
# -----------------------------
def render_bm_tile(bm):
    tags_html = "".join([
        f"""
        <span style="
            background:{get_tag_color(tag)};
            padding:6px 10px;
            border-radius:8px;
            margin-right:6px;
            font-size:0.8em;
            display:inline-block;
            color:#111;
        ">{tag}</span>
        """
        for tag in bm.get("tags", [])
    ])

    rev_html = "".join([
        f"<li style='margin-bottom:4px;color:#333;font-size:0.9em;'>{r}</li>"
        for r in bm.get("revenue_streams", [])
    ])

    use_html = "".join([
        f"<li style='margin-bottom:4px;color:#333;font-size:0.9em;'>{u}</li>"
        for u in bm.get("use_cases", [])
    ])

    ex_html = "".join([
        f"<li style='margin-bottom:4px;color:#333;font-size:0.9em;'>{x}</li>"
        for x in bm.get("examples", [])
    ])

    risk_html = "".join([
        f"<li style='margin-bottom:4px;color:#333;font-size:0.9em;'>{r}</li>"
        for r in bm.get("risks", [])
    ])

    # Card HTML block
    return f"""
    <div style="
        background:#FFFFFF;
        border:1px solid #DDD;
        border-radius:12px;
        padding:22px;
        margin-bottom:22px;
        box-shadow:0 2px 6px rgba(0,0,0,0.05);
    ">
        <h3 style="margin-bottom:4px;color:#111;">{bm['name']}</h3>
        <span style="color:#666;font-size:0.85em;">{bm['id']}</span>

        <p style="margin-top:12px;color:#333;">
            {bm.get('description', '')}
        </p>

        <div style="margin:12px 0;">{tags_html}</div>

        <div style="
            display:flex;
            justify-content:space-between;
            font-size:0.85em;
            color:#444;
            margin-top:10px;
        ">
            <div><strong>Difficulty:</strong> {bm.get('difficulty', '-')} / 5</div>
            <div><strong>Capex:</strong> {bm.get('capital_requirement', '-')}</div>
        </div>

        <div style="font-size:0.85em;color:#444;margin-top:8px;">
            <strong>Time to Revenue:</strong> {bm.get('time_to_revenue', '-')}
        </div>

        <hr style="margin:16px 0;border:0;border-top:1px solid #EEE;">

        <div style="margin-top:8px;">
            <strong style="color:#111;">Revenue Streams</strong>
            <ul style='margin-top:6px;margin-bottom:12px;padding-left:22px;'>
                {rev_html}
            </ul>
        </div>

        <div style="margin-top:8px;">
            <strong style="color:#111;">Use Cases</strong>
            <ul style='margin-top:6px;margin-bottom:12px;padding-left:22px;'>
                {use_html}
            </ul>
        </div>

        <div style="margin-top:8px;">
            <strong style="color:#111;">Examples</strong>
            <ul style='margin-top:6px;margin-bottom:12px;padding-left:22px;'>
                {ex_html}
            </ul>
        </div>

        <div style="margin-top:8px;">
            <strong style="color:#111;">Risks</strong>
            <ul style='margin-top:6px;margin-bottom:12px;padding-left:22px;'>
                {risk_html}
            </ul>
        </div>
    </div>
    """


# -----------------------------
# TAG COLOUR SYSTEM
# -----------------------------
TAG_COLORS = {
    "software": "#E3F2FD",
    "platform": "#E8EAF6",
    "AI": "#FCE4EC",
    "recurring": "#E8F5E9",
    "data": "#FFF3E0",
    "innovation": "#E1F5FE",
    "green": "#E8F5E9",
    "impact": "#E0F2F1",
    "hardware": "#F3E5F5",
    "manufacturing": "#FBE9E7",
    "finance": "#E0F7FA",
    "B2B": "#E8F5E9",
    "B2C": "#FFFDE7",
    "VR": "#F3E5F5",
    "cloud": "#E3F2FD",
    "transaction": "#F1F8E9",
}

def get_tag_color(tag):
    return TAG_COLORS.get(tag, "#EFEFEF")


# -----------------------------
# FILTERS
# -----------------------------
st.markdown("### Filters")

colA, colB, colC = st.columns(3)

# maturity level filter
maturity_filter = colA.multiselect(
    "Maturity Level",
    options=sorted(set([m["maturity_level"] for m in models])),
)

# difficulty filter
difficulty_filter = colB.slider(
    "Difficulty (0–5)",
    min_value=0, max_value=5, value=(0, 5)
)

# tag filter
tag_filter = colC.multiselect(
    "Tags",
    options=sorted({tag for m in models for tag in m.get("tags", [])}),
)


# -----------------------------
# APPLY FILTERS
# -----------------------------
filtered = models

if maturity_filter:
    filtered = [m for m in filtered if m["maturity_level"] in maturity_filter]

filtered = [m for m in filtered if difficulty_filter[0] <= m.get("difficulty", 0) <= difficulty_filter[1]]

if tag_filter:
    filtered = [m for m in filtered if any(t in tag_filter for t in m.get("tags", []))]


# -----------------------------
# RENDER RESULTS
# -----------------------------
st.markdown(f"### Showing {len(filtered)} of {len(models)} models\n")

cols = st.columns(3)

i = 0
for bm in filtered:
    with cols[i % 3]:
        st.markdown(render_bm_tile(bm), unsafe_allow_html=True)
    i += 1


