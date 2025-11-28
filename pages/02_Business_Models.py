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

# ---------------------------------------------------
# 1. Build Archetypes Based on Tags (auto-grouping)
# ---------------------------------------------------
ARHETYPES = {
    "AI & Data": ["AI", "data"],
    "Software (SaaS, Apps)": ["software", "recurring"],
    "Platforms & Ecosystems": ["platform"],
    "Finance & Funding Models": ["finance"],
    "Green & Impact Models": ["green", "impact"],
    "Manufacturing & Hardware": ["hardware", "manufacturing", "IoT"],
    "Retail / B2C Models": ["B2C", "retail"],
    "Innovation / Research": ["early_stage", "innovation", "research"],
}

def match_archetype(bm, selected_tags):
    return any(tag in bm["tags"] for tag in selected_tags)


# ---------------------------------------------------
# 2. User selects archetype
# ---------------------------------------------------
st.subheader("Select a Business Model Archetype")

selected_arch = st.selectbox(
    "Choose a category",
    list(ARHETYPES.keys()),
)

selected_tags = ARHETYPES[selected_arch]

# Filter models for this archetype
filtered_models = [
    bm for bm in BUSINESS_MODELS
    if match_archetype(bm, selected_tags)
]

st.markdown("---")
st.subheader(f"Models in: {selected_arch}")
st.markdown("Choose a model and expand to learn more.")

# ---------------------------------------------------
# 3. Card Design (same beautiful tile layout)
# ---------------------------------------------------

TAG_COLOURS = {
    "AI": "#DCE7FF",
    "software": "#FFE8D9",
    "platform": "#E9FFD9",
    "innovation": "#F4E5FF",
    "impact": "#E0F7FA",
    "finance": "#FFF4D6",
    "manufacturing": "#FFE6E6",
    "green": "#E0FFE6",
    "B2B": "#E8E8FF",
    "B2C": "#FFF2E8",
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


NUM_COLUMNS = 3
cols = st.columns(NUM_COLUMNS)

for idx, bm in enumerate(filtered_models):
    col = cols[idx % NUM_COLUMNS]

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

        with st.expander("Learn More"):
            st.markdown("### Revenue Streams")
            for r in bm.get("revenue_streams", []):
                st.markdown(f"- {r}")

            st.markdown("### Use Cases")
            for u in bm.get("use_cases", []):
                st.markdown(f"- {u}")

            st.markdown("### Examples")
            st.write(", ".join(bm.get("examples", [])))

            st.markdown("### Risks")
            for r in bm.get("risks", []):
                st.markdown(f"- {r}")
