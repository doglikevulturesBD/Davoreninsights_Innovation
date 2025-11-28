import streamlit as st
import json
import os

st.set_page_config(page_title="Business Models", layout="wide")

DATA_PATH = os.path.join("data", "business_models.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    MODELS = json.load(f)

st.title("Business Model Explorer")

# Archetype filtering
archetypes = sorted(list({t for m in MODELS for t in m["tags"]}))
selected = st.selectbox("Select an archetype:", ["All"] + archetypes)

if selected == "All":
    filtered = MODELS
else:
    filtered = [m for m in MODELS if selected in m["tags"]]

# Search
query = st.text_input("Search models:", "")

if query:
    filtered = [m for m in filtered if query.lower() in m["name"].lower()]

st.divider()

# Render models
for bm in filtered:

    with st.container(border=True):

        st.subheader(bm["name"])
        st.caption(bm["id"])

        st.write(bm["description"])

        # Tags in a row
        tag_cols = st.columns(len(bm["tags"]))
        for i, tag in enumerate(bm["tags"]):
            tag_cols[i].markdown(f"🟦 **{tag}**")

        col1, col2 = st.columns(2)
        col1.write(f"**Difficulty:** {bm['difficulty']} / 5")
        col2.write(f"**Capex:** {bm['capital_requirement']}")

        st.write(f"**Time to revenue:** {bm['time_to_revenue']}")

        st.markdown("### Revenue Streams")
        st.write("\n".join([f"- {x}" for x in bm["revenue_streams"]]))

        st.markdown("### Use Cases")
        st.write("\n".join([f"- {x}" for x in bm["use_cases"]]))

        st.markdown("### Examples")
        st.write("\n".join([f"- {x}" for x in bm["examples"]]))

        st.markdown("### Risks")
        st.write("\n".join([f"- {x}" for x in bm["risks"]]))

        st.divider()


