import streamlit as st

st.title("💡 Financial Literacy for Innovators")
st.write("A simple, visual guide to help innovators understand the financial concepts that matter for early-stage ventures.")

st.markdown("---")

# --- Topic Selection ---
topic = st.selectbox(
    "Choose a concept to explore:",
    [
        "Revenue Models",
        "Cost Structure",
        "Cashflow Literacy",
        "Unit Economics",
        "Profitability & Margins",
        "Funding Pathways",
        "Valuation Basics",
        "IRR / NPV / Payback (Conceptual)",
        "Risk & Sensitivity"
    ]
)

st.markdown("")

# ------------------------------------------------------------
# 1. REVENUE MODELS
# ------------------------------------------------------------
if topic == "Revenue Models":
    st.header("🔷 Revenue Models")

    st.info("Revenue models explain **how your innovation actually makes money**. They shape scalability, investor interest, and long-term sustainability.")

    st.subheader("Types of Revenue Models")

    st.success("**1. Recurring Revenue** — predictable monthly/annual income.\nExamples: SaaS, maintenance plans, memberships")

    st.success("**2. One-Off Sales** — sell a product once.\nExamples: hardware, kits, devices")

    st.success("**3. Usage-Based Revenue** — pay per unit consumed.\nExamples: kWh billing, API calls, pay-per-click")

    st.success("**4. Licensing & Royalties** — earn from IP without manufacturing.\nExamples: patented battery design licensed to OEMs")

    st.success("**5. Platform Commissions** — take a cut of marketplace transactions.\nExamples: Airbnb, Upwork")

    st.markdown("---")

    st.subheader("Why It Matters")
    st.write("""
    - Determines **scalability**  
    - Impacts **valuation**  
    - Influences **funding pathways**  
    - Dictates **risk and resource requirements**  
    """)

# ------------------------------------------------------------
# 2. COST STRUCTURE
# ------------------------------------------------------------
if topic == "Cost Structure":
    st.header("🧾 Cost Structure")

    st.info("Every innovation has two main cost categories: **CAPEX** and **OPEX**.")

    st.success("**CAPEX (Capital Expenditure)** — once-off large investments.\nExamples: equipment, tooling, deployment, hardware")

    st.success("**OPEX (Operating Expenditure)** — ongoing monthly costs.\nExamples: staff, hosting, transport, consumables")

    st.subheader("Fixed vs Variable Costs")
    st.write("""
    - **Fixed costs:** salaries, rent  
    - **Variable costs:** materials, energy, transaction fees  
    """)

    st.subheader("Why This Matters")
    st.write("""
    Cost structure affects  
    - margin,  
    - pricing,  
    - breakeven,  
    - scalability,  
    and even whether the **business model is viable at all**.
    """)

# ------------------------------------------------------------
# 3. CASHFLOW LITERACY
# ------------------------------------------------------------
if topic == "Cashflow Literacy":
    st.header("💰 Cashflow Literacy")

    st.info("Cashflow is the **heartbeat** of any business. More companies die from cashflow problems than from low profits.")

    st.subheader("Three Types of Cashflow")
    st.success("**Operating Cashflow** — day-to-day business activity")
    st.success("**Investing Cashflow** — equipment or long-term assets")
    st.success("**Financing Cashflow** — funding, loans, grants")

    st.subheader("Why Cashflow Matters")
    st.write("""
    - Determines survival  
    - Indicates growth readiness  
    - Influences funding required  
    """)

# ------------------------------------------------------------
# 4. UNIT ECONOMICS
# ------------------------------------------------------------
if topic == "Unit Economics":
    st.header("📦 Unit Economics")

    st.info("Unit economics show if **each customer** or **each unit sold** is profitable.")

    st.success("**Contribution Margin** = Price – Variable Cost")

    st.write("If contribution margin is negative, the model **cannot scale**.")

    st.success("**Customer Acquisition Cost (CAC)** — cost to get one customer.")
    st.success("**Customer Lifetime Value (LTV)** — revenue expected from the customer over time.")

    st.write("Healthy businesses aim for **LTV > 3 × CAC**.")

# ------------------------------------------------------------
# 5. PROFITS & MARGINS
# ------------------------------------------------------------
if topic == "Profitability & Margins":
    st.header("📊 Profitability & Margins")

    st.info("Margins tell you whether you have a business or just a project.")

    st.success("**Gross Margin** = (Revenue – Direct Costs) / Revenue")
    st.success("**Net Margin** = Profit after all expenses")

    st.write("Higher margins = higher valuation.")

# ------------------------------------------------------------
# 6. FUNDING PATHWAYS
# ------------------------------------------------------------
if topic == "Funding Pathways":
    st.header("🚀 Funding Pathways")

    st.info("Different stages require different types of funding.")

    st.success("**Grants** — good for early R&D, prototypes, proof-of-concept")
    st.success("**Equity** — scaling, hiring, new markets")
    st.success("**Debt** — stable revenues, predictable cashflow")
    st.success("**Revenue-based finance** — repay as you earn")

# ------------------------------------------------------------
# 7. VALUATION BASICS
# ------------------------------------------------------------
if topic == "Valuation Basics":
    st.header("📈 Valuation Basics")

    st.write("Valuation is about: risk, revenue, team, traction, and market size.")

    st.success("High recurring revenue → higher valuation")
    st.success("High scalability → higher valuation")
    st.success("Strong IP → higher valuation")

# ------------------------------------------------------------
# 8. IRR/NPV/PAYBACK (CONCEPTS ONLY)
# ------------------------------------------------------------
if topic == "IRR / NPV / Payback (Conceptual)":
    st.header("🧠 Investment Metrics (Conceptual)")

    st.write("No maths needed. Just the meaning:")

    st.success("**IRR** — the % return the project earns per year")
    st.success("**NPV** — value today of future revenue")
    st.success("**Payback** — how long until the investment is recovered")

# ------------------------------------------------------------
# 9. RISK & SENSITIVITY
# ------------------------------------------------------------
if topic == "Risk & Sensitivity":
    st.header("⚠️ Risk & Sensitivity")

    st.write("Sensitivity analysis tells you which assumptions matter most.")

    st.success("“What happens if revenue drops by 20%?”")
    st.success("“What if costs double?”")
    st.success("“What if customer adoption is slower?”")

    st.write("Investors love founders who understand risk early.")

st.markdown("---")
st.write("✨ More modules coming soon…")

