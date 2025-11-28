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

# ---- Sidebar Filters ----
st.sidebar.header("Filters")

# Unique maturity levels and tags
all_maturity = sorted(list({bm["maturity_level"] for bm in BUSINESS_MODELS}))
all_tags = sorted(list({tag for bm in BUSINESS_MODELS for tag in bm["tags"]}))

selected_maturity = st.sidebar.multiselect(
    "Filter by maturity level",
    all_maturity,
)

selected_tags = st.sidebar.multiselect(
    "Filter by tags",
    all_tags,
)

# ---- Filtering Logic ----
def passes_filters(bm):
    if selected_maturity and bm["maturity_level"] not in selected_maturity:
        return False
    if selected_tags and not any(tag in bm["tags"] for tag in selected_tags):
        return False
    return True

filtered_models = [bm for bm in BUSINESS_MODELS if passes_filters(bm)]

# ---- Display Cards ----
st.write(f"### Showing {len(filtered_models)} of {len(BUSINESS_MODELS)} models")

for bm in filtered_models:
    with st.container():
        st.markdown(
            f"""
            <div style="
                border:1px solid #ddd;
                padding:18px;
                border-radius:12px;
                margin-bottom:20px;
                background-color:#fafafa;
            ">
                <h3>{bm["name"]} <span style='font-size:0.8em;color:#777;'>({bm["id"]})</span></h3>
                <p style="color:#333;">{bm["description"]}</p>
            """,
            unsafe_allow_html=True
        )

        # Metrics Row
        col1, col2, col3 = st.columns(3)
        col1.metric("Difficulty", f"{bm.get('difficulty', '-')}/5")
        col2.metric("Capital Need", bm.get("capital_requirement", "-"))
        col3.metric("Time to Revenue", bm.get("time_to_revenue", "-"))

        # Tags as chips
        st.markdown("**Tags:**")
        tag_html = " ".join(
            [f"<span style='background:#e0f0ff;padding:6px;border-radius:6px;margin-right:4px;font-size:0.8em;'>{t}</span>"
             for t in bm["tags"]]
        )
        st.markdown(tag_html, unsafe_allow_html=True)

        # Revenue Streams
        if bm.get("revenue_streams"):
            st.markdown("**Revenue Streams:**")
            for item in bm["revenue_streams"]:
                st.markdown(f"- {item}")

        # Use Cases
        if bm.get("use_cases"):
            st.markdown("**Use Cases:**")
            for item in bm["use_cases"]:
                st.markdown(f"- {item}")

        # Examples
        if bm.get("examples"):
            st.markdown("**Examples:**")
            st.markdown(", ".join(bm["examples"]))

        # Risks
        if bm.get("risks"):
            st.markdown("**Risks:**")
            for item in bm["risks"]:
                st.markdown(f"- {item}")

        st.markdown("</div>", unsafe_allow_html=True)


