import streamlit as st
import numpy as np
import pandas as pd

st.title("📘 Financial Concepts for Innovators")
st.write("Learn the core financial tools used in evaluating business models and technology projects.")

st.markdown("---")

# ---- Topic selection ----
topic = st.selectbox(
    "Choose a topic to explore:",
    [
        "Internal Rate of Return (IRR)",
        "Net Present Value (NPV)",
        "Payback Period",
        "Cashflow Basics",
    ]
)

st.markdown("")

# ----------------------------------------
#          IRR SECTION
# ----------------------------------------
if topic == "Internal Rate of Return (IRR)":
    st.header("📈 Internal Rate of Return (IRR)")

    st.write("""
    IRR tells you the **percentage return** a project earns over time.
    It is the discount rate at which the **NPV becomes zero**.
    """)

    st.subheader("🎓 Example Project")
    st.write("Adjust the sliders to see how IRR changes.")

    capex = st.slider("Initial Cost (CAPEX)", 10_000, 2_000_000, 500_000, 10_000)
    years = st.slider("Project Duration (years)", 1, 15, 7)
    annual_return = st.slider("Annual Cash Inflow", 10_000, 500_000, 120_000, 5_000)

    cashflows = [-capex] + [annual_return] * years

    try:
        irr = np.irr(cashflows)
        st.metric("Calculated IRR", f"{irr*100:.2f}%")
    except:
        st.metric("Calculated IRR", "Not computable")

    df = pd.DataFrame({
        "Year": list(range(0, years + 1)),
        "Cashflow": cashflows
    })

    st.write("### Cashflow Table")
    st.dataframe(df)

    st.write("### Cumulative Cashflow")
    st.line_chart(df["Cashflow"].cumsum())

    st.info("""
    **Interpretation**
    - IRR > discount rate → Good  
    - IRR < discount rate → Not attractive  
    - Higher IRR = faster capital recovery  
    """)

# ----------------------------------------
#          NPV SECTION
# ----------------------------------------
if topic == "Net Present Value (NPV)":
    st.header("💰 Net Present Value (NPV)")

    st.write("""
    NPV measures the **value today** of all future cashflows.
    It answers: *Is this project worth more than it costs?*
    """)

    capex = st.slider("Initial Cost", 10_000, 2_000_000, 600_000, 10_000)
    discount = st.slider("Discount Rate (%)", 1, 20, 8) / 100
    years = st.slider("Years", 1, 15, 7)
    annual_return = st.slider("Annual Cash Inflow", 10_000, 500_000, 150_000, 5_000)

    cashflows = [-capex] + [annual_return] * years
    npv = np.npv(discount, cashflows)

    st.metric("NPV Result", f"R {npv:,.2f}")

    df = pd.DataFrame({
        "Year": list(range(0, years+1)),
        "Cashflow": cashflows
    })

    st.write("### Cashflow Table")
    st.dataframe(df)

    st.write("### Cumulative Cashflow")
    st.line_chart(df["Cashflow"].cumsum())

    st.success("""
    **Interpretation**  
    - NPV > 0 → Project creates value  
    - NPV < 0 → Project destroys value  
    """)

# ----------------------------------------
#          PAYBACK PERIOD
# ----------------------------------------
if topic == "Payback Period":
    st.header("⏳ Payback Period")

    st.write("""
    Payback period measures **how long it takes to recover the initial investment**.
    """)

    capex = st.slider("CAPEX", 10_000, 1_000_000, 300_000)
    years = st.slider("Years", 1, 15, 6)
    annual_return = st.slider("Annual Inflow", 10_000, 300_000, 80_000)

    cashflows = [-capex] + [annual_return] * years
    cumulative = np.cumsum(cashflows)

    payback = next((i for i, val in enumerate(cumulative) if val >= 0), None)

    st.metric("Payback Period", f"{payback} years" if payback else "No payback")

    df = pd.DataFrame({"Year": range(len(cashflows)), "Cashflow": cashflows, "Cumulative": cumulative})
    st.dataframe(df)

    st.line_chart(df["Cumulative"])

    st.info("""
    **Interpretation**  
    - Shorter payback ⇒ lower risk  
    - Does not show profitability after payback  
    """)

# ----------------------------------------
#          CASHFLOW BASICS
# ----------------------------------------
if topic == "Cashflow Basics":
    st.header("💡 Cashflow Basics")

    st.write("""
    Cashflow is the foundation of all financial projections.  
    It's simply **money in minus money out**.
    """)

    revenue = st.slider("Monthly Revenue", 1_000, 200_000, 50_000)
    opex = st.slider("Monthly Costs", 1_000, 150_000, 20_000)

    monthly_cf = revenue - opex
    st.metric("Monthly Cashflow", f"R {monthly_cf:,.2f}")

    values = [monthly_cf * i for i in range(13)]

    st.write("### 12-Month Cashflow Growth")
    st.line_chart(values)

    st.info("""
    **Interpretation**
    - Positive cashflow means sustainability  
    - Negative cashflow requires funding or burn management  
    - All business models depend on consistent cashflow  
    """)

st.markdown("---")
st.write("✨ More educational modules coming soon…")

