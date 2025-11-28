import streamlit as st
import json

st.title("📘 Business Models Learning Library")

# -----------------------------------
# Load Data
# -----------------------------------
with open("data/business_models.json", "r") as f:   # you said you renamed it back
    BUSINESS_MODELS = json.load(f)

# -----------------------------------
# Optional search (for ease)
# -----------------------------------
search = st.text_input("Search models", "")

if search:
    FILTERED = [bm for bm in BUSINESS_MODELS if search.lower() in bm["name"].lower() or search.lower() in bm["description"].lower()]
else:
    FILTERED = BUSINESS_MODELS

st.markdown("---")

# -----------------------------------
# CARD STYLE VIEW
# -----------------------------------
for bm in FILTERED:

    # Top section
    st.markdown(f"## {bm['name']}")
    st.markdown(f"*{bm['description']}*")

    # Metrics Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Difficulty", bm.get("difficulty", "-").title())
    col2.metric("Capital Needed", bm.get("capital_requirement", "-").title())
    col3.metric("Time to Revenue", bm.get("time_to_revenue", "-").title())

    # Tags row
    st.caption(f"**Tags:** {', '.join(bm['tags'])}")
    st.caption(f"**Maturity Level:** {bm['maturity_level'].title()}")

    # Expandable detailed sections
    with st.expander("📌 Revenue Streams"):
        for r in bm.get("revenue_streams", []):
            st.markdown(f"- {r}")

    with st.expander("📌 Typical Use Cases"):
        for u in bm.get("use_cases", []):
            st.markdown(f"- {u}")

    with st.expander("📌 Real-World Examples"):
        for e in bm.get("examples", []):
            st.markdown(f"- {e}")

    with st.expander("📌 Risks & Challenges"):
        for r in bm.get("risks", []):
            st.markdown(f"- {r}")

    st.markdown("---")

