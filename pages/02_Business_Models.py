import streamlit as st

st.title("Business Models — Education Module")
st.caption("Davoren Insights: Learning → Tools → Application")

st.markdown("---")

# -------------------------
# INTRO
# -------------------------
st.header("What Is a Business Model?")
st.write("""
A business model explains **how your innovation creates value, delivers value, and captures value**.

Most innovators jump immediately into technology — but investors always ask:
**“How will you make money, and why will this work?”**

Understanding business models helps you:
- position your technology correctly  
- avoid unrealistic paths  
- focus on a repeatable strategy  
- match your TRL and funding stage  
""")

st.info("""
A great business model = repeatable + scalable + defendable.
""")

st.markdown("---")

# -------------------------
# CORE BUSINESS MODEL CATEGORIES
# -------------------------
st.header("The 8 Major Business Model Archetypes")
st.write("Most real business models fit into one or a combination of these 8 categories.")

bm_categories = {
    "1. Recurring / Subscription Models": """
    **Examples:** SaaS, membership, recurring fees  
    **Strength:** Predictable revenue  
    **Best for:** Software, analytics, digital communities  
    """,

    "2. Platform & Marketplace Models": """
    **Examples:** marketplaces, crowdsourcing, ecosystem orchestrators  
    **Strength:** Network effects  
    **Best for:** B2B/B2C platforms, transaction-based systems  
    """,

    "3. Data & AI Monetisation Models": """
    **Examples:** DaaS, predictive analytics, AI-as-a-service  
    **Strength:** High scalability  
    **Best for:** Analytics tools, ML/AI startups  
    """,

    "4. Hardware / Infrastructure Models": """
    **Examples:** Hardware-as-a-service, OEM, energy services  
    **Strength:** Strong defensibility  
    **Best for:** IoT, energy tech, industrial systems  
    """,

    "5. Impact & Sustainability Models": """
    **Examples:** carbon credits, circular economy, impact-linked loans  
    **Strength:** Grant + investment blend  
    **Best for:** Climate innovations, ESG-focused ventures  
    """,

    "6. Finance & Hybrid Investment Models": """
    **Examples:** blended finance, royalty, revenue share models  
    **Strength:** Works for high-risk deep tech  
    **Best for:** TRL 4–9 enterprises  
    """,

    "7. Manufacturing & Production Models": """
    **Examples:** white-label, OEM, digital manufacturing networks  
    **Strength:** Scales with demand  
    **Best for:** physical products, engineering companies  
    """,

    "8. Creator & Digital Experience Models": """
    **Examples:** content platforms, gamification, VR experiences  
    **Strength:** Low CAPEX  
    **Best for:** creators, edtech, VR/AR innovators  
    """,
}

for category, desc in bm_categories.items():
    with st.expander(category):
        st.markdown(desc)

st.markdown("---")

# -------------------------
# HOW TO CHOOSE THE RIGHT BUSINESS MODEL
# -------------------------
st.header("How to Choose the Right Business Model")
st.write("""
Your business model must match:

1. **Your TRL**  
   - TRL 1–3 → concepts with licensing, grants, research  
   - TRL 4–6 → hybrid models, pilot revenue, early partnerships  
   - TRL 7–9 → recurring, platform, product sales, services  

2. **Your capital availability**  
   - Low capital → digital, subscription, data  
   - Medium → platform, consulting-to-product  
   - High → hardware, infrastructure, ESCO, OEM  

3. **Your innovation’s nature**  
   - Software → SaaS, freemium, platform  
   - Hardware → HaaS, OEM, leasing  
   - Impact → carbon credits, circular models  
   - AI → AI-as-a-service, predictive analytics  

4. **Your market type (B2B, B2C, public sector)**  
""")

st.success("""
**Rule of thumb:**  
The business model must fit the *physics* of your innovation — not the other way around.
""")

st.markdown("---")

# -------------------------
# LINK TO THE MENTOR TOOL
# -------------------------
st.info("""
### 👉 Apply this knowledge to your own idea  
Use the **Business Model Selector** inside the *Innovation Mentor* app
to generate your personalised top 3 recommendations based on your innovator archetype.

**Open Innovation Mentor → Business Model Tool**
""")

st.markdown("---")

# -------------------------
# OPTIONAL YOUTUBE EMBED
# -------------------------
st.header("Video Explainer (Coming Soon)")
st.write("A short 3–5 minute breakdown of common business models will appear here.")
st.write("Once uploaded, we can embed your YouTube link here.")


# -------------------------
# OPTIONAL DOWNLOAD
# -------------------------
st.download_button(
    label="Download Business Model Summary",
    data="Business Model Summary Placeholder",
    file_name="business_model_summary.txt"
)

