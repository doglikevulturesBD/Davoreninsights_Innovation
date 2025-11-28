import streamlit as st
import json

st.title("📘 Business Models Education Explorer")

# ---------------------------------------
# Load Data
# ---------------------------------------
with open("data/business_models_v2.json", "r") as f:
    BUSINESS_MODELS = json.load(f)

# ---------------------------------------
# Filters & Search
# ---------------------------------------
st.sidebar.header("Filters")

search_term = st.sidebar.text_input("Search", "")

difficulty_filter = st.sidebar.multiselect(
    "Difficulty",
    ["low", "medium", "high"]
)

capital_filter = st.sidebar.multiselect(
    "Capital Requirement",
    ["low", "medium", "high"]
)

time_filter = st.sidebar.multiselect(
    "Time to Revenue",
    ["fast", "medium", "slow"]
)

maturity_filter = st.sidebar.multiselect(
    "Maturity Level",
    ["emerging", "established", "dominant"]
)

# ---------------------------------------
# Filtering Logic
# ---------------------------------------
def passes_filters(bm):
    if search_term:
        term = search_term.lower()
        if term not in bm["name"].lower() and term not in bm["description"].lower():
            return False

    if difficulty_filter and bm["difficulty"] not in difficulty_filter:
        return False

    if capital_filter and bm["capital_requirement"] not in capital_filter:
        return False

    if time_filter and bm["time_to_revenue"] not in time_filter:
        return False

    if maturity_filter and bm["maturity_level"] not in maturity_filter:
        return False

    return True


DISPLAY_MODELS = [bm for bm in BUSINESS_MODELS if passes_filters(bm)]

# ---------------------------------------
# Display as Beautiful Educational Tiles
# ---------------------------------------
st.markdown(f"### Showing {len(DISPLAY_MODELS)} business models")

cols = st.columns(3)

for idx, bm in enumerate(DISPLAY_MODELS):
    with cols[idx % 3]:
        st.markdown(f"#### {bm['name']}")
        st.caption(bm["description"])

        st.write(f"**Difficulty:** {bm['difficulty'].title()}")
        st.write(f"**Capital:** {bm['capital_requirement'].title()}")
        st.write(f"**Time to Revenue:** {bm['time_to_revenue'].title()}")

        with st.expander("More Details"):
            st.markdown("**Revenue Streams:**")
            for r in bm.get("revenue_streams", []):
                st.markdown(f"- {r}")

            st.markdown("**Use Cases:**")
            for r in bm.get("use_cases", []):
                st.markdown(f"- {r}")

            st.markdown("**Examples:**")
            for e in bm.get("examples", []):
                st.markdown(f"- {e}")

            st.markdown("**Risks:**")
            for r in bm.get("risks", []):
                st.markdown(f"- {r}")

            st.caption(f"Tags: {', '.join(bm['tags'])}")

    st.markdown("---")


