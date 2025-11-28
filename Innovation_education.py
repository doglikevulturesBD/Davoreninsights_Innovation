import streamlit as st

st.set_page_config(
    page_title="Davoren Insights — Education",
    page_icon="📘",
    layout="wide"
)

# -------------------------------
# HEADER
# -------------------------------
st.title("📘 Davoren Insights — Education")
st.write("Your learning hub for innovation, commercialisation, and energy systems.")

st.markdown("---")

# -------------------------------
# CATEGORY GRID
# -------------------------------
st.subheader("Explore Learning Paths")

categories = {
    "Business Models": "📊",
    "TRL Levels": "🧪",
    "Commercialisation Strategy": "🚀",
    "IP & Patents": "📜",
    "Energy Systems": "⚡",
    "Carbon Markets": "🌍",
    "Batteries & EV": "🔋",
    "Data, AI & Simulation": "🤖"
}

cols = st.columns(4)

i = 0
for name, icon in categories.items():
    with cols[i % 4]:
        st.markdown(
            f"""
            <div style='padding:20px; border-radius:10px; background:#F7F7F7; text-align:center'>
                <h2 style='margin-bottom:0;'>{icon}</h2>
                <p style='font-size:18px;'>{name}</p>
                <a href='./{str(i+1).zfill(2)}_{name.replace(" ", "_")}' 
                    style='text-decoration:none;'>
                    <button style='padding:8px 16px; border-radius:6px; border:none; background:#4A90E2; color:white; cursor:pointer;'>
                        Start Learning
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )
    i += 1

st.markdown("---")

# -------------------------------
# LINKS TO OTHER PARTS OF ECOSYSTEM
# -------------------------------
st.subheader("Davoren Insights Ecosystem")

st.markdown("""
- 💡 **Innovation Mentor Tool** – Practical tools for innovators  
- 🧰 **Davoren Insights Tools Suite** – TRL calculator, business model selector, etc.  
- 🎥 **YouTube Channel** – Bite-sized video explainers  
- ✍️ **Blog** – In-depth articles and insights  
""")
