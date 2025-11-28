import streamlit as st
import json
import os

st.title("Business Model Library")

# ---- Load JSON ----
DATA_PATH = "data/business_models.json"

if not os.path.exists(DATA_PATH):
    st.error(f"Missing file: {DATA_PATH}")
    st.stop()

with open(DATA_PATH, "r", encoding="utf-8") as f:
    BUSINESS_MODELS = json.load(f)

# ----------- Colour Map for Category Tags ----------
TAG_COLOURS = {
    "AI": "#DCE7FF",
    "software": "#FFE8D9",
    "platform": "#E9FFD9",
    "innovation": "#F4E5FF",
    "impact": "#E0F7FA",
    "finance": "#FFF4D6",
    "manufacturing": "#FFE6E6",
    "green": "#E0FFE6",
}

def tag_chip(tag):
    colour = TAG_COLOURS.get(tag, "#f0f0f0")
    return f"""
    <span style="
        background:{colour};
        padding:6px 10px;
        border-radius:8px;
        margin-right:6px;
        font-size:0.8em;
        color:#333;
    ">{tag}</span>
    """

# ---- Tiled Grid Layout ----
NUM_COLUMNS = 3
cols = st.columns(NUM_COLUMNS)

for idx, bm in enumerate(BUSINESS_MODELS):
    col = cols[idx % NUM_COLUMNS]  # choose which column to put the tile in

    with col:
        st.markdown(
            f"""
            <div style="
                background:white;
                border-radius:12px;
                padding:18px;
                margin-bottom:20px;
                border:1px solid #e5e5e5;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            ">
                <h3 style="margin-bottom:0px;">{bm['name']}</h3>
                <span style="color:#888;font-size:0.9em;">{bm['id']}</span><br><br>
                <p style="color:#444;min-height:60px;">{bm['description']}</p>

                <div style="margin-bottom:10px;">
                    {" ".join([tag_chip(t) for t in bm['tags']])}
                </div>

                <div style="
                    display:flex;
                    justify-content:space-between;
                    font-size:0.8em;
                    color:#444;
                    margin-top:10px;
                ">
                    <div><strong>Difficulty:</strong> {bm.get('difficulty','-')}/5</div>
                    <div><strong>Capex:</strong> {bm.get('capital_requirement','-')}</div>
                </div>

                <div style="
                    font-size:0.8em;
                    color:#444;
                    margin-top:4px;
                ">
                    <strong>Time to Rev:</strong> {bm.get('time_to_revenue','-')}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Expandable details (prevents long scroll)
        with st.expander("Learn More"):
            st.markdown(f"**Revenue Streams**")
            for r in bm.get("revenue_streams", []):
                st.markdown(f"- {r}")

            st.markdown(f"**Use Cases**")
            for u in bm.get("use_cases", []):
                st.markdown(f"- {u}")

            st.markdown(f"**Examples**")
            st.write(", ".join(bm.get("examples", [])))

            st.markdown(f"**Risks**")
            for r in bm.get("risks", []):
                st.markdown(f"- {r}")

