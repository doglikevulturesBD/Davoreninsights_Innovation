import streamlit as st
import math


st.set_page_config(page_title="Financial Literacy for Innovators", layout="wide")

st.title("📊 Financial Literacy for Innovators")
st.caption("A practical, non-intimidating overview of the numbers behind your innovation.")


# ---------- Helper Functions ----------

def compute_npv(cash_flows, discount_rate):
    """cash_flows: list of (t, cf), discount_rate in decimal"""
    npv = 0.0
    for t, cf in cash_flows:
        npv += cf / ((1 + discount_rate) ** t)
    return npv


def compute_irr(cash_flows, tol=1e-4, max_iter=1000):
    """Basic IRR solver via binary search"""
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

# ---------- TAB 1: Costs ----------
with tabs[0]:
    st.subheader("1. Costs – Know Your Financial Foundation")

    st.markdown("""
    Understanding your **cost structure** is the foundation of financial literacy.  
    Every innovation, no matter how technical, is sitting on a cost stack.
    """)

    st.markdown("""
    | Type           | Meaning                          | Examples                                  | Why It Matters                            |
    |----------------|----------------------------------|-------------------------------------------|-------------------------------------------|
    | **Fixed**      | Don’t change with units sold     | Salaries, rent, insurance, software       | Sets your monthly survival cost           |
    | **Variable**   | Increase per unit                | Materials, packaging, lab time            | Determines your unit margin               |
    | **Semi-variable** | Mixed behaviour               | Cloud services, utilities                 | Grows with usage but not linearly         |
    | **Hidden**     | Often forgotten                  | Retesting, failed prototypes, delivery    | Quiet killers                             |
    """)

    st.markdown("### Quick Calculator")

    col1, col2 = st.columns(2)
    with col1:
        fixed_costs = st.number_input("Monthly fixed costs (R)", 0.0, 50000.0)
        var_cost = st.number_input("Variable cost per unit (R)", 0.0, 200.0)
    with col2:
        price = st.number_input("Selling price per unit (R)", 0.0, 500.0)
        expected_units = st.number_input("Expected monthly units", 0, 100)

    margin = price - var_cost
    st.write(f"- Margin per unit: **R{margin:,.2f}**")

    if margin > 0:
        breakeven_units = fixed_costs / margin
        st.write(f"- Break-even units per month: **{breakeven_units:,.1f} units**")
    else:
        st.warning("Selling price must be higher than variable cost.")

# ---------- TAB 2: Pricing ----------
with tabs[1]:
    st.subheader("2. Pricing – Don’t Undervalue Your Idea")

    st.markdown("""
    | Method        | Best For                       | Logic                                  |
    |---------------|--------------------------------|----------------------------------------|
    | **Cost-Plus** | Hardware, manufacturing         | Price = Cost + Markup                  |
    | **Value-Based** | High-value tech               | Price = Portion of value created       |
    | **Benchmark** | Crowded markets                | Compare competitors & adjust           |
    """)

    st.markdown("### Value-Based Pricing Helper")

    col1, col2, col3 = st.columns(3)
    with col1:
        annual_saving = st.number_input("Annual customer saving (R)", 0.0, 120000.0)
    with col2:
        share = st.slider("Charge % of value created", 1, 50, 20)
    with col3:
        years = st.number_input("Contract length (years)", 1, 1)

    total_value = annual_saving * years
    suggested_price = total_value * (share / 100)

    st.write(f"- Total value created: **R{total_value:,.0f}**")
    st.write(f"- Suggested price: **R{suggested_price:,.0f}**")


# ---------- TAB 3: Cash Flow ----------
with tabs[2]:
    st.subheader("3. Cash Flow – What Actually Keeps You Alive")
    st.markdown("**Profit is opinion, cash is fact.**")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        revenue = st.number_input("Monthly revenue (R)", 0.0, 150000.0)
    with col2:
        variable = st.number_input("Monthly variable costs (R)", 0.0, 60000.0)
    with col3:
        fixed = st.number_input("Monthly fixed costs (R)", 0.0, 50000.0)
    with col4:
        cash = st.number_input("Cash in bank (R)", 0.0, 300000.0)

    gross = revenue - variable
    net = gross - fixed
    burn = max(variable + fixed - revenue, 0)
    runway = (cash / burn) if burn > 0 else float("inf")

    st.write(f"- Gross profit: **R{gross:,.0f}**")
    st.write(f"- Net profit: **R{net:,.0f}**")
    st.write(f"- Burn rate: **R{burn:,.0f}**")
    if burn > 0:
        st.write(f"- Runway: **{runway:,.1f} months**")
    else:
        st.success("No burn rate at current values.")


# ---------- TAB 4: DCF & NPV ----------
with tabs[3]:
    st.subheader("4. Discounted Cash Flow (DCF) & Net Present Value (NPV)")

    col_top = st.columns(3)
    with col_top[0]:
        initial = st.number_input("Initial investment (Year 0, R)", 0.0, 200000.0)
    with col_top[1]:
        years = st.slider("Years", 1, 10, 5)
    with col_top[2]:
        rate = st.slider("Discount rate (%)", 1, 40, 12)

    st.markdown("### Enter Future Cash Flows")
    cf_cols = st.columns(years)
    flows = []
    for i in range(years):
        with cf_cols[i]:
            val = st.number_input(f"Year {i+1}", key=f"y{i+1}", value=float(100000*(i+1)))
        flows.append(val)

    if st.button("Calculate NPV"):
        r = rate / 100
        cash_flows = [(0, -initial)] + [(t, cf) for t, cf in enumerate(flows, 1)]
        npv = compute_npv(cash_flows, r)

        st.write(f"**NPV = R{npv:,.2f}**")
        if npv > 0:
            st.success("Positive NPV — project adds value.")
        else:
            st.error("Negative NPV — project destroys value.")


# ---------- TAB 5: IRR ----------
with tabs[4]:
    st.subheader("5. Internal Rate of Return (IRR)")

    col_top = st.columns(2)
    with col_top[0]:
        irr_initial = st.number_input("Initial investment (R)", 0.0, 200000.0, key="i_initial")
    with col_top[1]:
        irr_years = st.slider("Years", 1, 10, 5, key="i_years")

    irr_cols = st.columns(irr_years)
    irr_flows = []
    for i in range(irr_years):
        with irr_cols[i]:
            val = st.number_input(f"Year {i+1}", value=float(100000*(i+1)), key=f"irr_y{i+1}")
        irr_flows.append(val)

    if st.button("Calculate IRR"):
        cash_flows = [(0, -irr_initial)] + [(t, cf) for t, cf in enumerate(irr_flows, 1)]
        irr = compute_irr(cash_flows)

        if irr is None:
            st.error("IRR cannot be computed for these cash flows.")
        else:
            irr_pct = irr * 100
            st.write(f"**IRR = {irr_pct:.2f}%**")
            if irr_pct > 20:
                st.success("Strong IRR for innovation.")
            elif irr_pct > 10:
                st.info("Reasonable IRR.")
            else:
                st.warning("Low IRR — recheck pricing and costs.")


# ---------- TAB 6: Valuation Tools ----------
with tabs[5]:
    st.subheader("6. Simple Valuation Tools")

    st.markdown("""
    | Method | Best For | Logic |
    |--------|----------|--------|
    | **Scorecard** | TRL 3–6 | Weighted score |  
    | **Comparables** | TRL 7+ | Market comps |
    | **DCF** | Revenue or strong pilots | Discount future cash |
    | **Multiples** | SaaS / platform | ARR × multiple |
    """)

    st.markdown("### Quick Scorecard Demo")
    colA, colB, colC, colD = st.columns(4)

    with colA:
        team = st.slider("Team strength", 0, 10, 7)
    with colB:
        ip = st.slider("IP strength", 0, 10, 6)
    with colC:
        traction = st.slider("Traction", 0, 10, 5)
    with colD:
        market = st.slider("Market size", 0, 10, 8)

    score = team*0.3 + ip*0.25 + traction*0.2 + market*0.25
    st.write(f"**Scorecard score: {score:.1f} / 10**")


# ---------- TAB 7: Risk & Scenarios ----------
with tabs[6]:
    st.subheader("7. Risk & Scenario Thinking")

    st.markdown("""
    | Risk | Example | Mitigation |
    |------|----------|-------------|
    | **Cost risk** | Supplier increases prices | Buffers, multiple suppliers |
    | **Revenue risk** | Customer delays | MoUs, early pilots |
    | **Scale risk** | System fails at volume | Staged roll-out |
    | **Cash flow risk** | Late payments | 50/50 upfront |
    """)

    st.markdown("### Scenario Explorer")
    base_rev = st.number_input("Base revenue (R)", 0.0, 1_000_000.0)
    base_cost = st.number_input("Base costs (R)", 0.0, 700_000.0)

    col_b, col_e, col_w = st.columns(3)

    with col_b:
        st.markdown("**Best Case**")
        rev_up = st.slider("Revenue +%", 0, 200, 30)
        cost_down = st.slider("Cost -%", 0, 50, 10)
        st.write(f"Profit: R{base_rev*(1+rev_up/100) - base_cost*(1-cost_down/100):,.0f}")

    with col_e:
        st.markdown("**Expected**")
        st.write(f"Profit: R{base_rev - base_cost:,.0f}")

    with col_w:
        st.markdown("**Worst Case**")
        rev_down = st.slider("Revenue -%", 0, 100, 30)
        cost_up = st.slider("Cost +%", 0, 100, 20)
        st.write(f"Profit: R{base_rev*(1-rev_down/100) - base_cost*(1+cost_up/100):,.0f}")


# ---------- TAB 8: Adjusted Revenue ----------
with tabs[7]:
    st.subheader("8. Adjusted Revenue")

    st.markdown("""
    Adjusted revenue includes external impact value:
    - Energy savings  
    - Carbon credits  
    - Licensing  
    - Other monetisable impact  
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        d = st.number_input("Direct revenue (R/yr)", 0.0, 1_000_000.0)
    with col2:
        s = st.number_input("Savings (R/yr)", 0.0, 150_000.0)
    with col3:
        c = st.number_input("Carbon credits (R/yr)", 0.0, 100_000.0)
    with col4:
        l = st.number_input("Licensing (R/yr)", 0.0, 80_000.0)

    adjusted = d + s + c + l
    st.write(f"**Adjusted Revenue: R{adjusted:,.0f}**")


# ---------- TAB 9: Financial Story ----------
with tabs[8]:
    st.subheader("9. Your 5-Sentence Financial Story")

    col1, col2 = st.columns(2)
    with col1:
        p = st.text_input("Problem cost?", "High energy bills for small factories.")
        v = st.text_input("Value delivered?", "We reduce energy spend by 20–30%.")
        pr = st.text_input("Pricing model?", "Monthly subscription + setup fee.")
    with col2:
        m = st.text_input("Margin logic?", "Low variable cost, cloud-based.")
        f = st.text_input("Funding unlocks?", "Scale to 50 clients + carbon revenue.")

    if st.button("Generate Story"):
        st.markdown("### Financial Story")
        st.write(f"1. Customers face the costly problem of **{p}**.")
        st.write(f"2. Our solution delivers value by **{v}**.")
        st.write(f"3. We generate revenue through **{pr}**.")
        st.write(f"4. Our margins are sustainable because **{m}**.")
        st.write(f"5. Funding will **{f}**, making the business commercially strong.")
