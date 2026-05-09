import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Afterschool Enrichment", layout="centered")

# --- Load image as base64 ---
def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

IMG = {
    "Language":       img_b64("data_ai/category_images/language.png"),
    "Life Skills":    img_b64("data_ai/category_images/life_skills.png"),
    "All":            img_b64("data_ai/category_images/all.png"),
    "Arts":           img_b64("data_ai/category_images/arts.png"),
    "STEM":           img_b64("data_ai/category_images/steam.png"),
    "Sports & Games": img_b64("data_ai/category_images/sports_games.png"),
}

ICONS = {
    "Language": "🗣️", "Life Skills": "💡", "All": "📋",
    "Arts": "🎨", "STEM": "🔬", "Sports & Games": "🏆",
}

# --- Global Styles ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
h1, h2, h3, h4 {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    color: #2d3a6b !important;
}

/* Make the card image + overlay button work together */
.card-wrap {
    position: relative;
    width: 100%;
    margin-bottom: 12px;
    cursor: pointer;
}
.card-wrap img {
    width: 100%;
    border-radius: 14px;
    display: block;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.card-wrap:hover img {
    transform: scale(1.03);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
.card-wrap .card-btn {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    opacity: 0;
    cursor: pointer;
}
/* Invisible overlay button */
.card-wrap > div[data-testid="stButton"] {
    position: absolute !important;
    top: 0 !important; left: 0 !important;
    width: 100% !important; height: 100% !important;
    z-index: 10;
}
.card-wrap > div[data-testid="stButton"] > button {
    width: 100% !important;
    height: 100% !important;
    opacity: 0 !important;
    cursor: pointer !important;
    border: none !important;
    background: transparent !important;
}

/* Active card highlight */
.card-active img {
    box-shadow: 0 0 0 4px #3d5a99 !important;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 📚 Afterschool Enrichment Activities")
st.caption("Click a category below to explore online programs and compare costs.")

df = pd.read_csv("data_ai/afterschool_activities.csv")

# --- Filters ---
col_a, col_b, col_c = st.columns(3)
with col_a:
    age_groups = ["All Ages"] + sorted(df["Age Group"].unique().tolist())
    selected_age = st.selectbox("Age Group", age_groups)
with col_b:
    skill_levels = ["All Levels"] + sorted(df["Skill Level"].unique().tolist())
    selected_skill = st.selectbox("Skill Level", skill_levels)
with col_c:
    min_cost, max_cost = int(df["Cost Per Month"].min()), int(df["Cost Per Month"].max())
    cost_range = st.slider("Monthly Cost ($)", min_cost, max_cost, (min_cost, max_cost))

# --- Apply Filters ---
filtered = df.copy()
if selected_age != "All Ages":
    filtered = filtered[filtered["Age Group"] == selected_age]
if selected_skill != "All Levels":
    filtered = filtered[filtered["Skill Level"] == selected_skill]
filtered = filtered[
    (filtered["Cost Per Month"] >= cost_range[0]) &
    (filtered["Cost Per Month"] <= cost_range[1])
]

st.markdown("---")

if len(filtered) == 0:
    st.info("No activities match your filters.")
    st.stop()

# --- Session state ---
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"

# --- Clickable image cards (2-column grid) ---
st.markdown("#### Select a Category")

card_order = [
    ("Language",       "Life Skills"),
    ("All",            "Arts"),
    ("STEM",           "Sports & Games"),
]

for left_cat, right_cat in card_order:
    col1, col2 = st.columns(2)

    for col, cat in [(col1, left_cat), (col2, right_cat)]:
        active_class = "card-active" if st.session_state.selected_category == cat else ""
        with col:
            st.markdown(f'<div class="card-wrap {active_class}">', unsafe_allow_html=True)
            st.markdown(
                f'<img src="data:image/png;base64,{IMG[cat]}" alt="{cat}">',
                unsafe_allow_html=True
            )
            if st.button(" ", key=f"card_{cat}", use_container_width=True):
                st.session_state.selected_category = cat
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

active = st.session_state.selected_category
icon = ICONS.get(active, "📋")
st.markdown(f"### {icon} {active if active != 'All' else 'All Categories'}")

# --- Sort ---
sort_options = {
    "Cost: Low to High": ("Cost Per Month", True),
    "Cost: High to Low": ("Cost Per Month", False),
    "Name A–Z":          ("Activity Name", True),
}
sort_choice = st.selectbox("Sort by", list(sort_options.keys()), label_visibility="collapsed")
sort_col, sort_asc = sort_options[sort_choice]
filtered = filtered.sort_values(sort_col, ascending=sort_asc)

# --- Activities ---
CATEGORIES = ["Language", "Life Skills", "Arts", "STEM", "Sports & Games"]
display_categories = [active] if active != "All" else CATEGORIES

for category in display_categories:
    cat_data = filtered[filtered["Category"] == category]
    if len(cat_data) == 0:
        continue

    if active == "All":
        st.markdown(f"#### {ICONS[category]} {category}")

    for _, row in cat_data.iterrows():
        cost_label = "Free" if row["Cost Per Month"] == 0 else f"${row['Cost Per Month']}/mo"
        with st.expander(f"{row['Activity Name']} — {cost_label}"):
            c1, c2 = st.columns([3, 2])
            with c1:
                st.write(row["Description"])
                st.caption(f"Provider: {row['Provider']}")
            with c2:
                st.write(f"**Ages:** {row['Age Group']}")
                st.write(f"**Level:** {row['Skill Level']}")
                st.write(f"**Schedule:** {row['Days Per Week']}x/week, {row['Duration (Hours)']} hr/session")

    st.markdown("")
