import streamlit as st
import math

st.set_page_config(page_title="Financial Literacy for Innovators", layout="wide")

st.title("📊 Financial Literacy for Innovators")
st.caption("A practical, non-intimidating overview of the numbers behind your innovation.")


# ---------- Helper Functions ----------

def compute_npv(cash_flows, discount_rate):
    npv = 0.0
    for t, cf in cash_flows:
        npv += cf / ((1 + discount_rate) ** t)
    return npv


def compute_irr(cash_flows, tol=1e-4, max_iter=1000):
    npv0 = compute_npv(cash_flows, 0.0)
    npv_high = compute_npv(cash_flows, 5.0)

    if npv0 * npv_high > 0:
        return None

    low, high = 0.0, 5.0
    for _ in range(max_iter):
        mid = (low + high) / 2
        npv_mid = compute_npv(cash_flows, mid)
        if abs(npv_mid) < tol:
            return mid
        if npv0 * npv_mid < 0:
            high = mid
        else:
            low = mid
    return None


# ---------- Tabs Layout ----------

tabs = st.tabs([
    "Costs",
    "Pricing",
    "Cash Flow",
    "DCF & NPV",
    "IRR",
    "Valuation Tools",
    "Risk & Scenarios",
    "Adjusted Revenue",
    "Financial Story",
])

# ------------------------------------------------------------------------------------
# TAB 1: COSTS
# ------------------------------------------------------------------------------------
with tabs[0]:
    st.subheader("1. Costs – Know Your Financial Foundation")

    st.markdown("""
    Understanding your **cost structure** is the foundation of financial literacy.
    """)

    st.markdown("""
    | Type | Meaning | Examples | Why It Matters |
    |------|---------|----------|----------------|
    | **Fixed** | Don’t change with units sold | Salaries, rent | Survival baseline |
    | **Variable** | Scale with units | Materials, packaging | Determines margin |
    | **Semi-variable** | Mixed | C
