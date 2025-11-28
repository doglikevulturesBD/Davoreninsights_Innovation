import json
import streamlit as st
from typing import List, Dict, Any

# ----------------------------
# Load business models
# ----------------------------
@st.cache_data
def load_business_models() -> List[Dict[str, Any]]:
    with open("data/business_models.json", "r") as f:
        return json.load(f)

business_models = load_business_models()

# ----------------------------
# Archetype definitions
# ----------------------------
ARCHETYPES = {
    "Digital & SaaS": [
        "software", "data", "AI", "cloud", "digital", "platform", "developer"
    ],
    "Hardware & Infrastructure": [
        "hardware", "infrastructure", "IoT", "manufacturing", "high_capex"
    ],
    "Finance & Funding": [
        "finance", "fund", "loan", "equity", "blended", "royalties"
    ],
    "Impact & Community": [
        "impact", "green", "sustainability", "community", "local", "cooperative"
    ],
    "IP, Knowledge & Services": [
        "IP", "research", "knowledge", "education", "services", "consulting"
    ],
}

ARCHETYPE_ORDER = list(ARCHETYPES.keys())


def score_for_archetype(bm: Dict[str, Any], archetype: str) -> int:
    """
    Simple overlap score between model tags and archetype tags.
    """
    tags = [t.lower() for t in bm.get("tags", [])]
    target_tags = [t.lower() for t in ARCHETYPES.get(archetype, [])]
    return sum(1 for t in tags if t in target_tags)


def filter_by_archetype(
    models: List[Dict[str, Any]], archetype: str, top_n: int = 5
) -> List[Dict[str, Any]]:
    """
    Return top N models most aligned with the chosen archetype.
    """
    scored = []
    for bm in models:
        s = score_for_archetype(bm, archetype)
        if s > 0:
            scored.append((s, bm))

    if not scored:
        # if nothing matches (shouldn’t really happen), just fall back
        return models[:top_n]

    # Sort: highest score first, then easier difficulty, then name
    scored.sort(
        key=lambda x: (
            -x[0],
            x[1].get("difficulty", 3),
            x[1].get("name", ""),
        )
    )
    return [bm for _, bm in scored[:top_n]]


def filter_by_search(
    models: List[Dict[str, Any]], query: str
) -> List[Dict[str, Any]]:
    """
    Filter models by free-text search over name, description, and tags.
    """
    if not query:
        return models

    q = query.lower().strip()
    results = []
    for bm in models:
        haystack = " ".join(
            [
                bm.get("id", ""),
                bm.get("name", ""),
                bm.get("description", ""),
                " ".join(bm.get("tags", [])),
            ]
        ).lower()
        if q in haystack:
            results.append(bm)
    return results


def render_model_card(bm: Dict[str, Any]) -> None:
    """
    Render a single business model as a Streamlit 'card'.
    Pure Streamlit — no HTML.
    """
    with st.container(border=True):
        # Header row
        col_title, col_id = st.columns([4, 1])
        with col_title:
            st.subheader(bm.get("name", "Unnamed model"))
        with col_id:
            st.caption(bm.get("id", ""))

        # Tags
        tags = bm.get("tags", [])
        if tags:
            st.caption("Tags: " + ", ".join(tags))

        # Description
        desc = bm.get("description", "")
        if desc:
            st.write(desc)

        # Metrics row
        col1, col2, col3 = st.columns(3)
        difficulty = bm.get("difficulty", None)
        capex = bm.get("capital_requirement", "-")
        time_to_revenue = bm.get("time_to_revenue", "-")

        with col1:
            if difficulty is not None:
                st.metric("Difficulty", f"{difficulty} / 5")
            else:
                st.metric("Difficulty", "-")
        with col2:
            st.metric("Capital requirement", str(capex))
        with col3:
            st.metric("Time to revenue", str(time_to_revenue))

        # Expanders for deeper teaching content
        rev = bm.get("revenue_streams", [])
        if rev:
            with st.expander("Revenue streams"):
                for item in rev:
                    st.write(f"- {item}")

        use_cases = bm.get("use_cases", [])
        if use_cases:
            with st.expander("Use cases"):
                for item in use_cases:
                    st.write(f"- {item}")

        examples = bm.get("examples", [])
        if examples:
            with st.expander("Example companies / analogues"):
                for item in examples:
                    st.write(f"- {item}")

        risks = bm.get("risks", [])
        if risks:
            with st.expander("Key risks and watch-outs"):
                for item in risks:
                    st.write(f"- {item}")


# ----------------------------
# Page layout
# ----------------------------
st.title("Business Model Library")

st.write(
    "Use this page to **learn** and **teach** different business model patterns. "
    "Start by choosing an archetype that feels closest to your innovation, or "
    "browse/search all 70 models."
)

# Archetype selection
st.markdown("### Step 1 – Choose your primary archetype")

arch_cols = st.columns(len(ARCHETYPE_ORDER))
selected_arch = None
for i, arch in enumerate(ARCHETYPE_ORDER):
    with arch_cols[i]:
        if st.button(arch, use_container_width=True):
            st.session_state["selected_archetype"] = arch

# Default archetype in state
if "selected_archetype" not in st.session_state:
    st.session_state["selected_archetype"] = ARCHETYPE_ORDER[0]

selected_arch = st.session_state["selected_archetype"]
st.info(f"Current archetype: **{selected_arch}**")

# Search + view-all controls
st.markdown("### Step 2 – Refine / explore")

col_search, col_toggle = st.columns([3, 1])
with col_search:
    search_query = st.text_input(
        "Search business models (name, tags, description)",
        placeholder="e.g. SaaS, carbon, community, franchise...",
    )
with col_toggle:
    show_all = st.checkbox("Show all 70 models", value=False)

# Decide which models to show
models_to_show: List[Dict[str, Any]]

if show_all:
    models_to_show = business_models
else:
    models_to_show = filter_by_archetype(
        business_models, selected_arch, top_n=5
    )

# Apply search on whatever base set we’re using
models_to_show = filter_by_search(models_to_show, search_query)

st.markdown("### Step 3 – Explore the models")

if not models_to_show:
    st.warning(
        "No business models match this combination of archetype and search. "
        "Try clearing the search text or switching archetype."
    )
else:
    for bm in models_to_show:
        render_model_card(bm)


