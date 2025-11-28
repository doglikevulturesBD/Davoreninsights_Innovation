import streamlit as st

st.title("Technology Readiness Levels (TRL) — Education Module")
st.caption("Davoren Insights: Learning → Tools → Application")

st.markdown("---")

# -------------------------
# INTRO
# -------------------------
st.header("What Are Technology Readiness Levels?")
st.write("""
Technology Readiness Levels (TRLs) provide a simple, universal language for describing *how mature* 
a technology or innovation is — from early concept to market-ready deployment.

If you understand TRLs, you understand **where you are**, **what is missing**, and **what comes next**.
""")

st.info("""
**Shortcut summary**  
- TRL 1–3 → *Science*  
- TRL 4–6 → *Engineering*  
- TRL 7–9 → *Market*
""")

st.markdown("---")


# -------------------------
# TRL DEFINITIONS
# -------------------------
st.header("The Nine TRL Levels — Explained Clearly")

trl_data = {
    "TRL 1 — Basic Principles Observed": """
    • Pure scientific exploration  
    • Curiosity-driven research  
    • No prototype, no design, no concept yet  
    """,

    "TRL 2 — Technology Concept Formulated": """
    • You've seen something interesting  
    • You can define a potential application  
    • Still no experimental proof  
    """,

    "TRL 3 — Experimental Proof-of-Concept": """
    • Laboratory validation  
    • Simulations, modelling, early experiments  
    • Digital twin or computational model is allowed  
    • You can *prove* the idea might work  
    """,

    "TRL 4 — Lab Validation of Components": """
    • Components tested together  
    • Bench setups  
    • Early integration begins  
    • Still controlled environment  
    """,

    "TRL 5 — Relevant Environment Validation": """
    • More representative conditions  
    • Environmental factors introduced  
    • Higher fidelity prototype  
    """,

    "TRL 6 — Prototype Demonstration": """
    • Full prototype  
    • Demonstrated in a relevant environment  
    • Can show performance under partial real-world conditions  
    """,

    "TRL 7 — System Prototype in Operational Environment": """
    • Pilot plant  
    • Live operational testing  
    • Integrated with real-world interfaces  
    """,

    "TRL 8 — Completed & Certified System": """
    • Technology is complete  
    • Certifications, compliance, validation tests  
    • Manufacturing process established  
    """,

    "TRL 9 — Market Deployment": """
    • Technology is in full operation  
    • Commercial adoption  
    • Scaling, replication, and business growth  
    """
}

for level, desc in trl_data.items():
    with st.expander(level, expanded=False):
        st.markdown(desc)


st.markdown("---")


# -------------------------
# HOW TO USE TRLs IN INNOVATION STRATEGY
# -------------------------
st.header("How TRLs Guide Your Innovation Strategy")
st.write("""
Understanding your TRL reveals:

- What evidence you still need  
- What investors expect at your stage  
- What type of funding fits you  
- What business model is realistic  
- Whether you should focus on research, engineering, or commercialisation  
""")

st.success("""
Examples:
• TRL 2–3 = Research grants, deep-tech incubators  
• TRL 4–6 = Engineering, prototyping, pilot funding  
• TRL 7–9 = Market funding, customers, manufacturing  
""")


# -------------------------
# CROSS-LINK TO INNOVATION MENTOR
# -------------------------
st.info("""
### 👉 Ready to apply this to your own innovation?
Use the **TRL Assessment Tool** inside the *Innovation Mentor* app to automatically measure your TRL and generate your readiness summary.

**Open Innovation Mentor → TRL Assessment**
""")


st.markdown("---")

# -------------------------
# OPTIONAL: ADD VIDEO
# -------------------------
st.header("Video Explainer (Coming Soon)")
st.write("Your TRL mini-lecture will appear here. You can embed a YouTube link once uploaded.")


# -------------------------
# OPTIONAL: DOWNLOAD SUMMARY
# -------------------------
st.download_button(
    label="Download TRL Summary (PDF coming soon)",
    data="TRL Summary text placeholder",
    file_name="TRL_summary.txt"
)

