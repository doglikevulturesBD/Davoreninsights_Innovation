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
    | **Semi-variable** | Mixed | Cloud, utilities | Impacts scaling |
    | **Hidden** | Often forgotten | Retesting, rework | Quiet killers |
    """)

    st.markdown("### Quick Calculator")

    col1, col2 = st.columns(2)
    with col1:
        fixed_costs = st.number_input("Monthly fixed costs (R)", min_value=0.0, value=50000.0,
                                      key="cost_fixed")
        var_cost = st.number_input("Variable cost per unit (R)", min_value=0.0, value=200.0,
                                   key="cost_variable")
    with col2:
        price = st.number_input("Selling price per unit (R)", min_value=0.0, value=500.0,
                                key="cost_price")
        expected_units = st.number_input("Expected units sold per month", min_value=0, value=100,
                                         key="cost_units")

    margin = price - var_cost
    st.write(f"- Margin per unit: **R{margin:,.2f}**")

    if margin > 0:
        breakeven_units = fixed_costs / margin
        st.write(f"- Break-even units: **{breakeven_units:,.1f} units/month**")
    else:
        st.warning("Selling price must exceed variable cost.")


# ------------------------------------------------------------------------------------
# TAB 2: PRICING
# ------------------------------------------------------------------------------------
with tabs[1]:
    st.subheader("2. Pricing – Don’t Undervalue Your Idea")

    st.markdown("""
    | Method | When It Works | Logic |
    |--------|----------------|--------|
    | **Cost-Plus** | Hardware | Price = Cost + Markup |
    | **Value-Based** | High-impact tech | Charge % of value created |
    | **Benchmark** | Crowded markets | Compare competitors |
    """)

    st.markdown("### Value-Based Pricing Helper")

    col1, col2, col3 = st.columns(3)
    with col1:
        annual_saving = st.number_input("Annual customer saving (R)", 0.0, 120000.0,
                                        key="pricing_saving")
    with col2:
        share = st.slider("Charge % of value created", 1, 50, 20,
                          key="pricing_share")
    with col3:
        years = st.number_input("Contract length (years)", 1, 1,
                                key="pricing_years")

    total_value = annual_saving * years
    suggested_price = total_value * (share / 100)

    st.write(f"- Total created value: **R{total_value:,.0f}**")
    st.write(f"- Suggested price: **R{suggested_price:,.0f}**")


# ------------------------------------------------------------------------------------
# TAB 3: CASH FLOW
# ------------------------------------------------------------------------------------
with tabs[2]:
    st.subheader("3. Cash Flow – What Actually Keeps You Alive")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        revenue = st.number_input("Monthly revenue (R)", 0.0, 150000.0, key="cf_rev")
    with col2:
        variable = st.number_input("Monthly variable costs (R)", 0.0, 60000.0, key="cf_var")
    with col3:
        fixed = st.number_input("Monthly fixed costs (R)", 0.0, 50000.0, key="cf_fixed")
    with col4:
        cash = st.number_input("Cash in bank (R)", 0.0, 300000.0, key="cf_cash")

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


# ------------------------------------------------------------------------------------
# TAB 4: DCF & NPV
# ------------------------------------------------------------------------------------
with tabs[3]:
    st.subheader("4. Discounted Cash Flow (DCF) & Net Present Value (NPV)")

    col_top = st.columns(3)
    with col_top[0]:
        initial = st.number_input("Initial investment (R)", 0.0, 200000.0,
                                  key="npv_initial")
    with col_top[1]:
        years = st.slider("Years of projection", 1, 10, 5,
                          key="npv_years")
    with col_top[2]:
        rate = st.slider("Discount rate (%)", 1, 40, 12,
                         key="npv_rate")

    st.markdown("### Cash Flows per Year")

    flows = []
    cf_cols = st.columns(years)
    for i in range(years):
        with cf_cols[i]:
            cf = st.number_input(f"Year {i+1}", value=float(100000*(i+1)),
                                 key=f"npv_year_{i+1}")
            flows.append(cf)

    if st.button("Calculate NPV", key="npv_button"):
        r = rate / 100
        cash_flows = [(0, -initial)] + [(t, cf) for t, cf in enumerate(flows, 1)]
        npv = compute_npv(cash_flows, r)

        st.write(f"**NPV = R{npv:,.2f}**")
        if npv > 0:
            st.success("Positive NPV — project adds value.")
        else:
            st.error("Negative NPV — project destroys value.")


# ------------------------------------------------------------------------------------
# TAB 5: IRR
# ------------------------------------------------------------------------------------
with tabs[4]:
    st.subheader("5. Internal Rate of Return (IRR)")

    col1, col2 = st.columns(2)
    with col1:
        irr_initial = st.number_input("Initial investment (R)", 0.0, 200000.0,
                                      key="irr_initial")
    with col2:
        irr_years = st.slider("Years", 1, 10, 5,
                              key="irr_years_slider")

    irr_flows = []
    irr_cols = st.columns(irr_years)
    for i in range(irr_years):
        with irr_cols[i]:
            val = st.number_input(f"Year {i+1}", value=float(100000*(i+1)),
                                  key=f"irr_year_cf_{i+1}")
            irr_flows.append(val)

    if st.button("Calculate IRR", key="irr_button"):
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
                st.info("Moderate IRR.")
            else:
                st.warning("Low IRR — revisit pricing and costs.")


# ------------------------------------------------------------------------------------
# TAB 6: VALUATION
# ------------------------------------------------------------------------------------
with tabs[5]:
    st.subheader("6. Simple Valuation Tools")

    st.markdown("""
    | Method | Best For | Logic |
    |--------|----------|--------|
    | **Scorecard** | TRL 3–6 | Weighted score |
    | **Comparables** | TRL 7+ | Market comps |
    | **DCF** | Revenue/pilots | Discounted cash |
    | **Multiples** | SaaS | ARR × multiple |
    """)

    st.markdown("### Quick Scorecard")

    colA, colB, colC, colD = st.columns(4)
    with colA:
        team = st.slider("Team strength", 0, 10, 7, key="val_team")
    with colB:
        ip = st.slider("IP strength", 0, 10, 6, key="val_ip")
    with colC:
        traction = st.slider("Traction", 0, 10, 5, key="val_traction")
    with colD:
        market = st.slider("Market size", 0, 10, 8, key="val_market")

    score = team*0.3 + ip*0.25 + traction*0.2 + market*0.25
    st.write(f"**Scorecard: {score:.1f} / 10**")


# ------------------------------------------------------------------------------------
# TAB 7: RISK & SCENARIOS
# ------------------------------------------------------------------------------------
with tabs[6]:
    st.subheader("7. Risk & Scenario Thinking")

    st.markdown("""
    | Risk | Example | Mitigation |
    |------|---------|-------------|
    | Cost | Supplier increases | Buffers |
    | Revenue | Customer delays | Pilots |
    | Scale | System fails at demand | Staged rollout |
    | Cash flow | Late payments | 50/50 upfront |
    """)

    st.markdown("### Scenario Explorer")

    base_rev = st.number_input("Base revenue (R)", 0.0, 1_000_000.0, key="sc_base_rev")
    base_cost = st.number_input("Base cost (R)", 0.0, 700_000.0, key="sc_base_cost")

    col_b, col_e, col_w = st.columns(3)

    with col_b:
        st.markdown("**Best Case**")
        rev_up = st.slider("Revenue +%", 0, 200, 30, key="sc_rev_up")
        cost_down = st.slider("Cost -%", 0, 50, 10, key="sc_cost_down")
        st.write(f"Profit: R{base_rev*(1+rev_up/100) - base_cost*(1-cost_down/100):,.0f}")

    with col_e:
        st.markdown("**Expected**")
        st.write(f"Profit: R{base_rev - base_cost:,.0f}")

    with col_w:
        st.markdown("**Worst Case**")
        rev_down = st.slider("Revenue -%", 0, 100, 30, key="sc_rev_down")
        cost_up = st.slider("Cost +%", 0, 100, 20, key="sc_cost_up")
        st.write(f"Profit: R{base_rev*(1-rev_down/100) - base_cost*(1+cost_up/100):,.0f}")


# ------------------------------------------------------------------------------------
# TAB 8: ADJUSTED REVENUE
# ------------------------------------------------------------------------------------
with tabs[7]:
    st.subheader("8. Adjusted Revenue")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        direct = st.number_input("Direct revenue (R/yr)", 0.0, 1_000_000.0,
                                 key="adj_direct")
    with col2:
        savings = st.number_input("Savings (R/yr)", 0.0, 150_000.0,
                                  key="adj_sav")
    with col3:
        carbon = st.number_input("Carbon credits (R/yr)", 0.0, 100_000.0,
                                 key="adj_carbon")
    with col4:
        licensing = st.number_input("Licensing (R/yr)", 0.0, 80_000.0,
                                    key="adj_lic")

    adjusted = direct + savings + carbon + licensing
    st.write(f"**Adjusted Revenue: R{adjusted:,.0f}**")


# ------------------------------------------------------------------------------------
# TAB 9: FINANCIAL STORY
# ------------------------------------------------------------------------------------
with tabs[8]:
    st.subheader("9. Your 5-Sentence Financial Story")

    col1, col2 = st.columns(2)
    with col1:
        p = st.text_input("Problem cost", "High energy bills for small factories.",
                          key="story_problem")
        v = st.text_input("Value delivered", "Reduce energy spend by 20–30%.",
                          key="story_value")
        pr = st.text_input("Pricing model", "Monthly subscription + setup fee.",
                           key="story_pricing")
    with col2:
        m = st.text_input("Margin logic", "Cloud-based, low variable cost.",
                          key="story_margin")
        f = st.text_input("Funding unlocks", "Scale to 50 clients + carbon revenue.",
                          key="story_fund")

    if st.button("Generate Financial Story", key="story_button"):
        st.markdown("### Financial Story")
        st.write(f"1. Customers face **{p}**.")
        st.write(f"2. Our solution provides value by **{v}**.")
        st.write(f"3. We generate revenue through **{pr}**.")
        st.write(f"4. Our margin model is strong because **{m}**.")
        st.write(f"5. Funding will **{f}**, improving commercial readiness.")
