import streamlit as st
import math

st.set_page_config(page_title="Financial Literacy for Innovators", layout="wide")

st.title("📊 Financial Literacy for Innovators")
st.caption("A complete educational module that teaches innovators core financial concepts using examples, visuals and interactive tools.")

# ================================================================
# Helper Functions
# ================================================================

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

# ================================================================
# Tabs
# ================================================================

tabs = st.tabs([
    "Costs",
    "Pricing",
    "Cash Flow",
    "DCF & NPV",
    "IRR",
    "Valuation",
    "Risk & Scenarios",
    "Adjusted Revenue",
    "Financial Story"
])

# ================================================================
# TAB 1 — COSTS
# ================================================================
with tabs[0]:
    st.header("1. Understanding Costs")

    st.markdown("""
### Why Costs Matter  
Costs determine:
- Your pricing strategy  
- Your break-even point  
- Your cash burn  
- How fast you scale  
- Whether the business survives  

There are four types of costs every innovator must understand:
""")

    with st.expander("📘 Cost Types Explained"):
        st.markdown("""
**1. Fixed Costs**  
Stay constant regardless of units sold.  
Examples: rent, salaries, admin fees, software subscriptions.

**2. Variable Costs**  
Increase with each unit sold.  
Examples: raw materials, packaging, energy, testing.

**3. Semi-variable Costs**  
Flat up to a point, then increase.  
Examples: cloud hosting tiers, electricity beyond a threshold.

**4. Hidden Costs**  
Most dangerous — often forgotten in planning.  
Examples: retesting, redesign, unexpected shipping, broken prototypes.
""")

    st.markdown("---")
    st.markdown("### 🔢 Break-even Calculator")

    col1, col2 = st.columns(2)
    with col1:
        fixed_costs = st.number_input("Monthly fixed costs (R)", min_value=0.0, value=60000.0, key="cost_fixed")
        var_cost = st.number_input("Variable cost per unit (R)", min_value=0.0, value=200.0, key="cost_var")
    with col2:
        price = st.number_input("Selling price per unit (R)", min_value=0.0, value=600.0, key="cost_price")
        units = st.number_input("Expected units sold per month", min_value=0, value=120, key="cost_units")

    margin = price - var_cost
    st.write(f"**Margin per unit:** R{margin:,.2f}")

    if margin > 0:
        breakeven = fixed_costs / margin
        st.success(f"Break-even point: **{breakeven:,.1f} units/month**")
    else:
        st.error("Selling price must exceed variable cost.")

# ================================================================
# TAB 2 — PRICING
# ================================================================
with tabs[1]:
    st.header("2. Pricing Strategies")

    st.markdown("""
Pricing affects:
- Profitability  
- Market adoption  
- Investor perception  
- Your ability to scale  
""")

    with st.expander("📘 Pricing Methods Explained"):
        st.markdown("""
**1. Cost-Plus Pricing**  
Simple: cost + markup.  
Best for physical products.

**2. Value-Based Pricing**  
Charge a percentage of the value your product creates.  
Best for high-impact innovation, energy savings, carbon reduction, manufacturing efficiency.

**3. Benchmark Pricing**  
Price in line with market alternatives.  
Useful for crowded markets.
""")

    st.markdown("---")
    st.markdown("### 🧮 Value-Based Pricing Helper")

    col1, col2, col3 = st.columns(3)
    with col1:
        saving = st.number_input("Annual saving created (R)", 0.0, 120000.0, key="pr_save")
    with col2:
        pct = st.slider("Percentage captured", 1, 50, 20, key="pr_pct")
    with col3:
        years = st.number_input("Contract length (years)", 1, 1, key="pr_years")

    total_value = saving * years
    suggested_price = total_value * (pct / 100)

    st.write(f"**Total created value:** R{total_value:,.0f}")
    st.success(f"Suggested value-based price: **R{suggested_price:,.0f}**")

# ================================================================
# TAB 3 — CASH FLOW
# ================================================================
with tabs[2]:
    st.header("3. Cash Flow Explained")

    st.markdown("""
Cash flow is more important than profit.  
Companies die because they run out of **cash**, not because of poor profit margins.

### 🔑 Key Concepts
- **Gross profit** = revenue – variable costs  
- **Net profit** = gross profit – fixed costs  
- **Burn rate** = monthly cash loss  
- **Runway** = months until cash runs out  

""")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        revenue = st.number_input("Monthly revenue (R)", min_value=0.0, value=150000.0, key="cf_rev")
    with col2:
        variable = st.number_input("Variable costs (R)", min_value=0.0, value=60000.0, key="cf_var")
    with col3:
        fixed = st.number_input("Fixed costs (R)", min_value=0.0, value=50000.0, key="cf_fix")
    with col4:
        cash = st.number_input("Cash available (R)", min_value=0.0, value=300000.0, key="cf_cash")

    gross = revenue - variable
    net = gross - fixed
    burn = max(variable + fixed - revenue, 0)
    runway = cash / burn if burn > 0 else float("inf")

    st.write(f"**Gross profit:** R{gross:,.0f}")
    st.write(f"**Net profit:** R{net:,.0f}")
    st.write(f"**Burn rate:** R{burn:,.0f}")

    if burn > 0:
        st.warning(f"Runway: **{runway:,.1f} months**")
    else:
        st.success("No burn — cash flow positive.")

# ================================================================
# TAB 4 — DCF & NPV
# ================================================================
with tabs[3]:
    st.header("4. DCF & NPV")

    st.markdown("""
### What is NPV?  
NPV tells you whether investing today is worth the future cash returns.

Positive NPV = good investment.  
Negative NPV = destroys value.

### Why innovators use NPV:
- To compare different investment options  
- To justify prototype or equipment spend  
- To evaluate scale-up decisions  
""")

    col_top = st.columns(3)
    with col_top[0]:
        initial = st.number_input("Initial investment (R)", 0.0, 200000.0, key="npv_init")
    with col_top[1]:
        years = st.slider("Years of projection", 1, 10, 5, key="npv_years")
    with col_top[2]:
        rate = st.slider("Discount rate (%)", 1, 40, 12, key="npv_rate")

    st.markdown("### Enter yearly cash flows")
    flows = []
    cols = st.columns(years)
    for i in range(years):
        with cols[i]:
            cf = st.number_input(f"Year {i+1}", value=float(100000*(i+1)), key=f"npv_cf_{i}")
            flows.append(cf)

    if st.button("Calculate NPV", key="npv_btn"):
        r = rate / 100
        cash_flows = [(0, -initial)] + [(t+1, flows[t]) for t in range(years)]
        npv = compute_npv(cash_flows, r)
        st.write(f"**NPV = R{npv:,.2f}**")
        st.success("Positive NPV — project adds value.") if npv > 0 else st.error("Negative NPV — project destroys value.")

# ================================================================
# TAB 5 — IRR
# ================================================================
with tabs[4]:
    st.header("5. Internal Rate of Return (IRR)")

    st.markdown("""
IRR shows the **effective annual return** of a project.  
Investors love IRR because it accounts for:
- Timing  
- Risk  
- Return  

> IRR > 20% = very attractive  
> IRR 10–20% = generally good  
""")

    col1, col2 = st.columns(2)
    with col1:
        irr_initial = st.number_input("Initial investment (R)", 0.0, 200000.0, key="irr_init")
    with col2:
        irr_years = st.slider("Years", 1, 10, 5, key="irr_years")

    irr_list = []
    cols = st.columns(irr_years)
    for i in range(irr_years):
        with cols[i]:
            val = st.number_input(f"Year {i+1}", value=float(100000*(i+1)), key=f"irr_cf_{i}")
            irr_list.append(val)

    if st.button("Calculate IRR", key="irr_btn"):
        cash_flows = [(0, -irr_initial)] + [(t+1, irr_list[t]) for t in range(irr_years)]
        irr = compute_irr(cash_flows)
        if irr is None:
            st.error("IRR could not be computed.")
        else:
            irr_pct = irr * 100
            st.write(f"**IRR = {irr_pct:.2f}%**")

# ================================================================
# TAB 6 — VALUATION
# ================================================================
with tabs[5]:
    st.header("6. Early-Stage Valuation")

    st.markdown("""
At TRL 3–6, valuation is based on:
- Team strength  
- IP defensibility  
- Market size  
- Traction  
- Technology advantage  

DCF is too early — scorecards are ideal.
""")

    colA, colB, colC, colD = st.columns(4)
    with colA: team = st.slider("Team", 0, 10, 7, key="val_team")
    with colB: ip = st.slider("IP strength", 0, 10, 6, key="val_ip")
    with colC: tr = st.slider("Traction", 0, 10, 5, key="val_tr")
    with colD: mk = st.slider("Market size", 0, 10, 8, key="val_mk")

    score = team*0.3 + ip*0.25 + tr*0.2 + mk*0.25
    st.success(f"Valuation Scorecard: **{score:.1f} / 10**")

# ================================================================
# TAB 7 — RISK & SCENARIOS
# ================================================================
with tabs[6]:
    st.header("7. Risk & Scenario Thinking")

    st.markdown("""
Scenario analysis helps innovators:
- Prepare for volatility  
- Adjust pricing or costs  
- Plan fundraising  
""")

    base_rev = st.number_input("Base revenue (R)", 0.0, 1_000_000.0, key="sc_rev")
    base_cost = st.number_input("Base cost (R)", 0.0, 700_000.0, key="sc_cost")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Best Case")
        inc = st.slider("Revenue +%", 0, 200, 30, key="sc_inc")
        dec = st.slider("Cost -%", 0, 50, 10, key="sc_dec")
        profit_best = base_rev*(1+inc/100) - base_cost*(1-dec/100)
        st.success(f"Profit: R{profit_best:,.0f}")

    with col2:
        st.markdown("### Expected")
        st.info(f"Profit: R{base_rev - base_cost:,.0f}")

    with col3:
        st.markdown("### Worst Case")
        down = st.slider("Revenue -%", 0, 100, 30, key="sc_down")
        up = st.slider("Cost +%", 0, 100, 20, key="sc_up")
        profit_worst = base_rev*(1-down/100) - base_cost*(1+up/100)
        st.error(f"Profit: R{profit_worst:,.0f}")

# ================================================================
# TAB 8 — ADJUSTED REVENUE
# ================================================================
with tabs[7]:
    st.header("8. Adjusted Revenue")

    st.markdown("""
Innovation often creates **indirect value**:
- Carbon credits  
- Energy savings  
- Licensing revenue  
- Social impact  
""")

    c1, c2, c3, c4 = st.columns(4)
    with c1: direct = st.number_input("Direct income (R/yr)", 0.0, 1_000_000.0, key="adj_dir")
    with c2: sav = st.number_input("Energy/cost savings", 0.0, 150000.0, key="adj_sav")
    with c3: carb = st.number_input("Carbon credits", 0.0, 100000.0, key="adj_car")
    with c4: lic = st.number_input("Licensing revenue", 0.0, 80000.0, key="adj_lic")

    adjusted = direct + sav + carb + lic
    st.success(f"Adjusted Revenue: **R{adjusted:,.0f}**")

# ================================================================
# TAB 9 — FINANCIAL STORY
# ================================================================
with tabs[8]:
    st.header("9. The Financial Story")

    st.markdown("""
A 5-sentence financial story communicates:
1. The cost of the problem  
2. The value delivered  
3. The pricing logic  
4. Why margins are sustainable  
5. What funding unlocks  

This is used for pitches, incubators, and funding agencies.
""")

    col1, col2 = st.columns(2)
    with col1:
        p = st.text_input("Problem cost", "High downtime and energy bills.")
        v = st.text_input("Value delivered", "Reduce peak consumption by 20–30%.")
        pr = st.text_input("Pricing model", "Hybrid hardware + subscription.")
    with col2:
        m = st.text_input("Margin logic", "Low variable cost once deployed.")
        f = st.text_input("Funding unlocks", "Scaling to 50 clients and local manufacturing.")

    if st.button("Generate Story"):
        st.info(f"1. Customers face: **{p}**.")
        st.info(f"2. We deliver value by: **{v}**.")
        st.info(f"3. We generate revenue through: **{pr}**.")
        st.info(f"4. Our margin model works because: **{m}**.")
        st.info(f"5. Funding will: **{f}**.")

