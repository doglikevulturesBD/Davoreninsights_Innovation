import streamlit as st
import json

# -------------------------------
# Load Data
# -------------------------------
with open("data/business_models.json", "r") as f:
    BUSINESS_MODELS = json.load(f)

with open("data/archetype_tags.json", "r") as f:
    ARCHETYPE_TAGS = json.load(f)

MATURITY_MAP = {
    "emerging": 0.3,
    "established": 0.6,
    "dominant": 1.0
}

# -------------------------------
# Scoring Function (v2)
# -------------------------------
def score_model(model, archetype_tags):
    tag_overlap = len(set(model["tags"]) & set(archetype_tags)) / len(model["tags"])
    maturity_w = MATURITY_MAP.get(model["maturity_level"], 0.5)

    # Simplified since success_score removed
    final_score = (0.7 * tag_overlap) + (0.3 * maturity_w)
    return final_score


# -------------------------------
# State Init
# -------------------------------
if "archetype" not in st.session_state:
    st.session_state["archetype"] = None

if "secondary_done" not in st.session_state:
    st.session_state["secondary_done"] = False


# -------------------------------
# UI Step 1: Choose Archetype
# -------------------------------
st.title("Business Model Explorer (v2)")

if st.session_state["archetype"] is None:
    st.subheader("1. Choose your Innovator Archetype")
    choice = st.radio(
        "Select the closest match to your profile:",
        list(ARCHETYPE_TAGS.keys())
    )

    if st.button("Continue"):
        st.session_state["archetype"] = choice
        st.rerun()

else:
    archetype = st.session_state["archetype"]
    st.success(f"Selected Archetype: **{archetype}**")

    archetype_tags = ARCHETYPE_TAGS[archetype]

    # -------------------------------
    # UI Step 2: Secondary Questions
    # -------------------------------
    if not st.session_state["secondary_done"]:
        st.subheader("2. Refine your profile")

        q1 = st.selectbox(
            "How fast do you want to commercialize?",
            ["Slow & Research-heavy", "Moderate", "Fast"]
        )

        q2 = st.selectbox(
            "Which is more important to you?",
            ["Recurring revenue", "Impact outcomes", "User scale", "Technology depth"]
        )

        q3 = st.selectbox(
            "What is your available startup capital?",
            ["Very low (< R50k)", "Medium", "High"]
        )

        if st.button("Generate Recommendations"):
            st.session_state["secondary_done"] = True
            st.session_state["q1"] = q1
            st.session_state["q2"] = q2
            st.session_state["q3"] = q3
            st.rerun()

    # -------------------------------
    # Step 3: Ranking + Display
    # -------------------------------
    if st.session_state["secondary_done"]:
        st.subheader("3. Recommended Business Models (Top 5)")

        # --- scoring ---
        results = []
        for model in BUSINESS_MODELS:
            score = score_model(model, archetype_tags)
            results.append((model, score))

        results = sorted(results, key=lambda x: x[1], reverse=True)
        top5 = results[:5]

        # ----------------------------------------
        # RICH CARD LAYOUT FOR TOP 5 MODELS
        # ----------------------------------------
        for bm, score in top5:
            st.markdown(f"## {bm['name']}")
            st.markdown(f"*{bm['description']}*")

            # --- Key attributes ---
            col1, col2, col3 = st.columns(3)
            col1.metric("Difficulty", bm.get("difficulty", "-").title())
            col2.metric("Capital Needed", bm.get("capital_requirement", "-").title())
            col3.metric("Time to Revenue", bm.get("time_to_revenue", "-").title())

            # --- Rich details ---
            st.markdown("### Revenue Streams")
            for r in bm.get("revenue_streams", []):
                st.markdown(f"- {r}")

            st.markdown("### Typical Use Cases")
            for u in bm.get("use_cases", []):
                st.markdown(f"- {u}")

            st.markdown("### Real-World Examples")
            for ex in bm.get("examples", []):
                st.markdown(f"- {ex}")

            st.markdown("### Risks & Challenges")
            for rk in bm.get("risks", []):
                st.markdown(f"- {rk}")

            st.markdown("---")

        # ----------------------------------------
        # SEE ALL MODELS (Simple list)
        # ----------------------------------------
        with st.expander("See all 70 business models"):
            for bm in BUSINESS_MODELS:
                st.markdown(f"### {bm['name']}")
                st.markdown(bm["description"])
                st.caption(f"Tags: {', '.join(bm['tags'])}")
                st.markdown("---")

