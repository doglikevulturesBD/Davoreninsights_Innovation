import streamlit as st
import math

st.set_page_config(page_title="Financial Literacy for Innovators", layout="wide")

st.title("📊 Financial Literacy for Innovators")
st.caption("A practical, non-intimidating overview of the numbers behind your innovation.")


# ---------- Helper Functions ----------

def compute_npv(cash_flows, discount_rate):
    """
    cash_flows: list of (t, cf) for t = 0,1,2,...
    discount_rate: decimal, e.g. 0.1 for 10%
    """
    npv = 0.0
    for t, cf in cash_flows:
        npv += cf / ((1 + discount_rate) ** t)
    return npv


def compute_irr(cash_flows, tol=1e-4, max_iter=1000):
    """
    Basic IRR via binary search.
    cash_flows: list of (t, cf) including t=0
    Returns IRR as decimal or None if cannot solve.
    """
    # Check if IRR is likely solvable (must have sign change)
    npv0 = compute_npv(cash_flows, 0.0)
    npv_high = compute_npv(cash_flows, 5.0)  # 500% discount as upper bound
    if npv0 * npv_high > 0:
        return None  # no sign change, probably no IRR in this range

    low, high = 0.0, 5.0
    for _ in range(max_iter):
        mid = (low + high) / 2
        npv_mid = compute_npv(cash_flows, mid)
        if abs(npv_mid) < tol:
            return mid
        if npv0 * npv_mid < 0:
            high = mid
            npv_high = npv_mid
        else:
            low = mid
            npv0 = npv_mid
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
    "Learning Scenarios (TRL → Finance)"
])

# ---------- TAB 1: Costs ----------
with tabs[0]:
    st.subheader("1. Costs – Know Your Financial Foundation")

    st.markdown("""
    Understanding your **cost structure** is the foundation of financial literacy.  
    Every innovation, no matter how technical, is sitting on a cost stack.
    """)

    st.markdown("### Cost Types")
    st.markdown("""
    | Type           | Meaning                          | Examples                                  | Why It Matters                            |
    |----------------|----------------------------------|-------------------------------------------|-------------------------------------------|
    | **Fixed**      | Don’t change with units sold     | Salaries, rent, insurance, software       | Sets your monthly survival cost           |
    | **Variable**   | Increase per unit                | Materials, packaging, shipping, lab time  | Determines your unit margin               |
    | **Semi-variable** | Mixed behaviour               | Cloud services, utilities                 | Grows with usage, but not linearly        |
    | **Hidden**     | Often forgotten                  | Rework, prototype failures, retesting     | Can quietly kill early-stage projects     |
    """)

    st.markdown("### Quick Calculator: Fixed vs Variable Mix")
    col1, col2 = st.columns(2)

    with col1:
        fixed_costs = st.number_input("Total monthly fixed costs (R)", min_value=0.0, value=50000.0, step=1000.0)
        variable_cost_per_unit = st.number_input("Variable cost per unit (R)", min_value=0.0, value=200.0, step=10.0)
    with col2:
        price_per_unit = st.number_input("Selling price per unit (R)", min_value=0.0, value=500.0, step=10.0)
        expected_units = st.number_input("Expected units sold per month", min_value=0, value=100, step=10)

    if price_per_unit > 0:
        margin_per_unit = price_per_unit - variable_cost_per_unit
    else:
        margin_per_unit = 0

    st.markdown("#### Results")
    st.write(f"- Margin per unit: **R{margin_per_unit:,.2f}**")
    if margin_per_unit > 0:
        break_even_units = fixed_costs / margin_per_unit if margin_per_unit else 0
        st.write(f"- Break-even units per month: **{break_even_units:,.1f} units**")
    else:
        st.warning("Set a selling price higher than your variable cost to get a meaningful margin.")


# ---------- TAB 2: Pricing ----------
with tabs[1]:
    st.subheader("2. Pricing – Don’t Undervalue Your Idea")

    st.markdown("""
    Your price should **tell a story**: the problem you solve and the value you create.

    ### Common Pricing Approaches
    | Method        | When It Works Best                  | Logic                                  | Notes                                   |
    |---------------|-------------------------------------|----------------------------------------|-----------------------------------------|
    | **Cost-Plus** | Hardware, manufacturing, simple B2B | Price = Cost + Markup%                 | Easy starting point                     |
    | **Value-Based** | Deep-tech, energy, medtech        | Price = Portion of value you create    | Best for high-impact innovation         |
    | **Benchmark** | Crowded markets, B2C                | Compare to competitors & adjust        | Prevents major over/under-pricing       |
    """)

    st.markdown("### Mini Value-Based Pricing Helper")
    col1, col2, col3 = st.columns(3)
    with col1:
        annual_saving = st.number_input("Estimated annual saving per customer (R)", min_value=0.0, value=120000.0, step=5000.0)
    with col2:
        share_of_value = st.slider("What % of that saving can you reasonably charge for?", min_value=1, max_value=50, value=20)
    with col3:
        contract_years = st.number_input("Typical contract length (years)", min_value=1, max_value=10, value=1)

    total_value = annual_saving * contract_years
    suggested_price = total_value * (share_of_value / 100)

    st.write(f"- Total value created over contract: **R{total_value:,.0f}**")
    st.write(f"- Suggested value-based price: **R{suggested_price:,.0f}**")


# ---------- TAB 3: Cash Flow ----------
with tabs[2]:
    st.subheader("3. Cash Flow – What Actually Keeps You Alive")

    st.markdown("""
    **Profit is a theory, cash is reality.**  
    Cash flow tells you how long you can survive and how fast you can grow.
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        monthly_revenue = st.number_input("Monthly revenue (R)", min_value=0.0, value=150000.0, step=5000.0)
    with col2:
        monthly_variable = st.number_input("Monthly variable costs (R)", min_value=0.0, value=60000.0, step=5000.0)
    with col3:
        monthly_fixed = st.number_input("Monthly fixed costs (R)", min_value=0.0, value=50000.0, step=5000.0)
    with col4:
        cash_in_bank = st.number_input("Cash in bank (R)", min_value=0.0, value=300000.0, step=10000.0)

    gross_profit = monthly_revenue - monthly_variable
    net_profit = gross_profit - monthly_fixed
    burn_rate = max(monthly_fixed + monthly_variable - monthly_revenue, 0)
    runway_months = (cash_in_bank / burn_rate) if burn_rate > 0 else math.inf

    st.markdown("### Summary")
    st.write(f"- Gross profit: **R{gross_profit:,.0f}** per month")
    st.write(f"- Net profit: **R{net_profit:,.0f}** per month")

    if burn_rate == 0:
        st.success("You are not burning cash at the current values (burn rate = 0).")
    else:
        st.write(f"- Burn rate: **R{burn_rate:,.0f}** per month")
        st.write(f"- Runway: **{runway_months:,.1f} months** at current burn rate")


# ---------- TAB 4: DCF & NPV ----------
with tabs[3]:
    st.subheader("4. Discounted Cash Flow (DCF) & Net Present Value (NPV)")

    st.markdown("""
    **DCF** estimates what your future cash flows are worth **today**.  
    **NPV** is the sum of those discounted cash flows minus the initial investment.

    > Rule of thumb: if **NPV > 0**, the project adds value (on your assumptions).
    """)

    col_top = st.columns(3)
    with col_top[0]:
        initial_investment = st.number_input("Initial investment (Year 0, R)", min_value=0.0, value=200000.0, step=10000.0)
    with col_top[1]:
        years = st.slider("Number of projection years", min_value=1, max_value=10, value=5)
    with col_top[2]:
        discount_rate_pct = st.slider("Discount rate (%)", min_value=1, max_value=40, value=12)

    st.markdown("### Estimated annual net cash flows (after all costs)")
    cash_flow_cols = st.columns(years)
    cash_flows_list = []
    for i in range(years):
        with cash_flow_cols[i]:
            cf = st.number_input(f"Year {i+1}", key=f"dcf_year_{i+1}", value=float(100000 * (i+1)), step=10000.0)
            cash_flows_list.append(cf)

    if st.button("Calculate NPV", key="calc_npv"):
        r = discount_rate_pct / 100.0
        cash_flows_t = [(0, -initial_investment)]
        for t, cf in enumerate(cash_flows_list, start=1):
            cash_flows_t.append((t, cf))

        npv_value = compute_npv(cash_flows_t, r)
        st.write(f"**NPV:** R{npv_value:,.2f}")

        if npv_value > 0:
            st.success("✅ Positive NPV: on these assumptions, the project creates value.")
        elif npv_value < 0:
            st.error("⚠️ Negative NPV: on these assumptions, the project destroys value.")
        else:
            st.info("NPV is approximately zero – borderline case.")


# ---------- TAB 5: IRR ----------
with tabs[4]:
    st.subheader("5. Internal Rate of Return (IRR)")

    st.markdown("""
    **IRR** is the discount rate at which **NPV = 0**.  
    It is a way of expressing the project’s return as a single %.

    > If **IRR is higher** than your required return (e.g. 12–15%), the project is attractive.
    """)

    st.markdown("Use the **same cash flows** as above or enter new ones:")

    col_irr_top = st.columns(2)
    with col_irr_top[0]:
        irr_initial_investment = st.number_input("Initial investment (Year 0, R)", min_value=0.0, value=200000.0, step=10000.0, key="irr_invest")
    with col_irr_top[1]:
        irr_years = st.slider("Projection years", min_value=1, max_value=10, value=5, key="irr_years")

    irr_cols = st.columns(irr_years)
    irr_cash_flows = []
    for i in range(irr_years):
        with irr_cols[i]:
            cf = st.number_input(f"Year {i+1}", key=f"irr_year_{i+1}", value=float(100000 * (i+1)), step=10000.0)
            irr_cash_flows.append(cf)

    if st.button("Calculate IRR", key="calc_irr"):
        cf_t = [(0, -irr_initial_investment)]
        for t, cf in enumerate(irr_cash_flows, start=1):
            cf_t.append((t, cf))

        irr_value = compute_irr(cf_t)
        if irr_value is None:
            st.error("Could not compute a meaningful IRR (cash flows may not produce a sign change in NPV).")
        else:
            st.write(f"**IRR:** {irr_value * 100:.2f}%")
            if irr_value * 100 > 20:
                st.success("Very strong IRR for an early-stage innovation (assuming assumptions are realistic).")
            elif irr_value * 100 > 10:
                st.info("Reasonable IRR for many innovation projects.")
            else:
                st.warning("IRR is relatively low. Re-check assumptions, cost base, and pricing.")


# ---------- TAB 6: Valuation Tools ----------
with tabs[5]:
    st.subheader("6. Simple Valuation Tools for Innovators")

    st.markdown("""
    For early TRL projects, valuation is **more about logic than precision**.

    | Method                | Best For                        | Logic                                      |
    |-----------------------|----------------------------------|-------------------------------------------|
    | **Scorecard**         | TRL 3–6, pre-revenue            | Weighted score for team, IP, traction     |
    | **Comparables**       | TRL 7+, early commercial        | Compare to similar startups                |
    | **DCF (NPV/IRR)**     | Revenue or strong pilots        | Discount future cash flows                 |
    | **Multiples (e.g. ARR)** | SaaS/platforms with revenue | Apply a sector multiple to annual revenue |
    """)

    st.markdown("### Quick Scorecard Demo")
    st.caption("Not a full valuation, but a way to structure your thinking.")
    colA, colB, colC, colD = st.columns(4)
    with colA:
        team = st.slider("Team strength (0–10)", 0, 10, 7)
    with colB:
        ip = st.slider("IP strength (0–10)", 0, 10, 6)
    with colC:
        traction = st.slider("Traction (0–10)", 0, 10, 5)
    with colD:
        market = st.slider("Market potential (0–10)", 0, 10, 8)

    score = team*0.3 + ip*0.25 + traction*0.2 + market*0.25
    st.write(f"**Scorecard score:** {score:.1f} / 10.0")
    st.caption("You can later map this score to a valuation range or funding readiness level in the broader app.")


# ---------- TAB 7: Risk & Scenarios ----------
with tabs[6]:
    st.subheader("7. Financial Risk & Scenario Thinking")

    st.markdown("""
    Every set of numbers should be tested under **different scenarios**.

    | Risk Type       | Example                                 | Mitigation                        |
    |-----------------|------------------------------------------|-----------------------------------|
    | **Cost risk**   | Supplier price spike                     | Buffers, alternative suppliers    |
    | **Revenue risk**| Customer delays adoption                 | Pilots, MoUs, staged rollouts     |
    | **Scale risk**  | System fails at higher volume            | Phased scale-up, testing          |
    | **Cash flow risk** | Late payments                        | Upfront deposits, milestone payments |
    """)

    st.markdown("### Simple Scenario Explorer")
    base_revenue = st.number_input("Base annual revenue (R)", min_value=0.0, value=1000000.0, step=50000.0)
    base_costs = st.number_input("Base annual total costs (R)", min_value=0.0, value=700000.0, step=50000.0)

    col_b, col_e, col_w = st.columns(3)
    with col_b:
        st.markdown("**Best Case**")
        rev_uplift = st.slider("Revenue +%", min_value=0, max_value=200, value=30, key="rev_up")
        cost_change_best = st.slider("Cost -%", min_value=0, max_value=100, value=10, key="cost_down")
        rev_best = base_revenue * (1 + rev_uplift/100)
        cost_best = base_costs * (1 - cost_change_best/100)
        st.write(f"Profit: R{rev_best - cost_best:,.0f}")

    with col_e:
        st.markdown("**Expected Case**")
        st.write(f"Revenue: R{base_revenue:,.0f}")
        st.write(f"Costs:   R{base_costs:,.0f}")
        st.write(f"Profit:  R{base_revenue - base_costs:,.0f}")

    with col_w:
        st.markdown("**Worst Case**")
        rev_drop = st.slider("Revenue -%", min_value=0, max_value=100, value=30, key="rev_down")
        cost_up = st.slider("Cost +%", min_value=0, max_value=100, value=20, key="cost_up")
        rev_worst = base_revenue * (1 - rev_drop/100)
        cost_worst = base_costs * (1 + cost_up/100)
        st.write(f"Profit: R{rev_worst - cost_worst:,.0f}")

    st.caption("Later you could replace this with a Monte Carlo module that randomly samples many such scenarios.")


# ---------- TAB 8: Adjusted Revenue ----------
with tabs[7]:
    st.subheader("8. Adjusted Revenue – Beyond Simple Sales")

    st.markdown("""
    For climate, energy, and impact projects, **revenue is more than just sales**.

    Adjusted revenue can include:
    - Direct product/service revenue  
    - Energy or cost savings  
    - Carbon credit revenue  
    - Licensing income  
    - Other externalities you can monetise
    """)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        direct_rev = st.number_input("Direct revenue (R/yr)", min_value=0.0, value=1000000.0, step=50000.0)
    with col2:
        savings = st.number_input("Energy / cost savings (R/yr)", min_value=0.0, value=150000.0, step=20000.0)
    with col3:
        carbon_rev = st.number_input("Carbon credits (R/yr)", min_value=0.0, value=100000.0, step=10000.0)
    with col4:
        licensing_rev = st.number_input("Licensing (R/yr)", min_value=0.0, value=80000.0, step=10000.0)
    with col5:
        other_rev = st.number_input("Other monetisable impacts (R/yr)", min_value=0.0, value=0.0, step=10000.0)

    adjusted_revenue = direct_rev + savings + carbon_rev + licensing_rev + other_rev

    st.write(f"**Adjusted annual revenue:** R{adjusted_revenue:,.0f}")
    st.caption("This concept ties nicely into your climate/impact lens and can feed into your DCF/NPV modules.")


# ---------- TAB 9: Financial Story ----------
with tabs[8]:
    st.subheader("9. Your 5-Sentence Financial Story")

    st.markdown("Fill in a few fields and the app composes a concise financial story for pitches or funding applications.")

    col1, col2 = st.columns(2)
    with col1:
        problem_cost = st.text_input("What costly problem do you solve?", "High energy bills for small manufacturers.")
        value_delivered = st.text_input("What is the main financial value?", "We cut energy costs by 20–30%.")
        pricing_model = st.text_input("How do you charge?", "Monthly subscription plus once-off setup fee.")
    with col2:
        margin_logic = st.text_input("Why are your margins sustainable?", "Cloud-based system with low variable costs.")
        funding_need = st.text_input("What does funding unlock?", "Scale to 50 customers and integrate carbon credit revenue.")

    if st.button("Generate Financial Story"):
        st.markdown("### Draft Financial Story")
        st.write(f"1. Our customers face the problem of **{problem_cost}**.")
        st.write(f"2. Our solution delivers financial value by **{value_delivered}**.")
        st.write(f"3. We generate revenue through **{pricing_model}**.")
        st.write(f"4. Our cost structure and margins are sustainable because **{margin_logic}**.")
        st.write(f"5. The funding we seek will **{funding_need}**, making the business financially and commercially robust.")


# ---------- TAB 10: Learning Scenarios (TRL → Finance) ----------
with tabs[9]:
    st.subheader("10. Learning Scenarios – From TRL to Finance")

    st.markdown("""
    This tab is for **teaching scenarios** that link your other app modules:
    - TRL Assessment  
    - Business Models  
    - IP & Licensing  
    - Financials & Risk  

    You can later connect this to real project data in your app.
    """)

    scenario = st.selectbox(
        "Choose a teaching scenario",
        [
            "Scenario 1: TRL 3 Lab Prototype",
            "Scenario 2: TRL 6 Field Pilot",
            "Scenario 3: TRL 8 Market-Ready Product"
        ],
    )

    if scenario == "Scenario 1: TRL 3 Lab Prototype":
        st.markdown("""
        **Scenario 1: TRL 3 – Lab Prototype**

        - **TRL Module:** Early-stage, high technical uncertainty, no revenue yet.  
        - **Business Model Module:** Still exploring options, use the business model selector to test patterns.  
        - **IP Module:** Focus on disclosures, prior art search, basic protection strategy.  
        - **Financial Focus:**  
          - Cost tracking (R&D, lab time, equipment)  
          - Very rough DCF set up for learning, not decision-making  
          - Simple scorecard valuation, not full NPV  
        - **Teaching Point:** At TRL 3, finance is about **cost discipline and future framing**, not detailed forecasting.
        """)

    elif scenario == "Scenario 2: TRL 6 Field Pilot":
        st.markdown("""
        **Scenario 2: TRL 6 – Field Pilot**

        - **TRL Module:** Real-world testing with pilot customers.  
        - **Business Model Module:** Narrow down to 1–2 realistic models (e.g. SaaS + hardware).  
        - **IP Module:** Filing decisions (patents/designs), early licensing conversations.  
        - **Financial Focus:**  
          - Use pilot data to estimate **realistic revenues and costs**  
          - Build first meaningful **NPV and IRR** models  
          - Introduce **scenario analysis** (best/expected/worst)  
        - **Teaching Point:** At TRL 6, finance becomes **evidence-based**. Numbers reflect data, not only assumptions.
        """)

    else:
        st.markdown("""
        **Scenario 3: TRL 8 – Market-Ready Product**

        - **TRL Module:** Near or at commercial launch.  
        - **Business Model Module:** Locked in, pricing tested with customers.  
        - **IP Module:** Protection in place, consider licensing opportunities and geographic expansion.  
        - **Financial Focus:**  
          - Full **DCF/NPV/IRR** for investors and funders  
          - Detailed **cash flow** and **runway planning**  
          - **Adjusted revenue** including savings, carbon, and licensing  
        - **Teaching Point:** At TRL 8, finance is about **scaling and investor readiness** – your story, numbers, and risk view must align.
        """)

    st.caption("Later, you can wire this tab to real project records in your app so learners can explore actual anonymised cases end-to-end.")

