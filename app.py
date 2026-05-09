import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Afterschool Enrichment", layout="centered")

def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

TITLE_IMG = img_b64("data_ai/category_images/title.png")

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

def cost_badge(cost):
    if cost == 0:
        return '<span style="background:#4CAF50;color:white;padding:2px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">FREE</span>'
    elif cost <= 29:
        return f'<span style="background:#8BC34A;color:white;padding:2px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">${cost}/mo</span>'
    elif cost <= 59:
        return f'<span style="background:#FF9800;color:white;padding:2px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">${cost}/mo</span>'
    else:
        return f'<span style="background:#e53935;color:white;padding:2px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">${cost}/mo</span>'

def mode_badge(mode):
    styles = {
        "Online":     "background:#1565C0;color:white",
        "In-Person":  "background:#2E7D32;color:white",
        "Hybrid":     "background:#6A1B9A;color:white",
    }
    style = styles.get(mode, "background:#555;color:white")
    return f'<span style="{style};padding:2px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">{mode}</span>'

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
h1, h2, h3, h4 {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    color: #2d3a6b !important;
}

/* Card image wrapper */
.card-wrap {
    position: relative;
    width: 100%;
    margin-bottom: 4px;
    cursor: pointer;
}
.card-wrap img.card-img {
    width: 100%;
    border-radius: 14px;
    display: block;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.card-wrap:hover img.card-img {
    transform: scale(1.03);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
.card-active img.card-img {
    box-shadow: 0 0 0 4px #3d5a99 !important;
    border-radius: 14px;
}

/* Count badge overlaid on card */
.count-badge {
    position: absolute;
    top: 10px;
    right: 12px;
    background: #2d3a6b;
    color: white;
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 0.85rem;
    padding: 2px 9px;
    border-radius: 20px;
    z-index: 5;
    pointer-events: none;
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
</style>
""", unsafe_allow_html=True)

st.markdown(
    f'<img src="data:image/png;base64,{TITLE_IMG}" style="width:100%;max-width:680px;display:block;margin:0 auto 4px auto;">',
    unsafe_allow_html=True
)
st.caption("Click a category card to explore programs and compare costs.")

df = pd.read_csv("data_ai/afterschool_activities.csv")

# --- Search bar ---
search = st.text_input("🔍 Search activities by name", placeholder="e.g. Coding, Chess, Spanish...")

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

col_d, col_e = st.columns(2)
with col_d:
    delivery_modes = ["All"] + sorted(df["Delivery Mode"].unique().tolist())
    selected_mode = st.selectbox("Delivery Mode", delivery_modes)
with col_e:
    locations = ["All Locations"] + sorted(df["Location"].unique().tolist())
    selected_location = st.selectbox("Location", locations)

# --- Apply Filters ---
filtered = df.copy()
if search:
    filtered = filtered[filtered["Activity Name"].str.contains(search, case=False, na=False)]
if selected_age != "All Ages":
    filtered = filtered[filtered["Age Group"] == selected_age]
if selected_skill != "All Levels":
    filtered = filtered[filtered["Skill Level"] == selected_skill]
if selected_mode != "All":
    filtered = filtered[filtered["Delivery Mode"] == selected_mode]
if selected_location != "All Locations":
    filtered = filtered[filtered["Location"] == selected_location]
filtered = filtered[
    (filtered["Cost Per Month"] >= cost_range[0]) &
    (filtered["Cost Per Month"] <= cost_range[1])
]

st.markdown("---")

if len(filtered) == 0:
    st.info("No activities match your search or filters.")
    st.stop()

if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# --- Helper: render one image card with count badge ---
def render_card(cat, count):
    active_class = "card-active" if st.session_state.selected_category == cat else ""
    st.markdown(f'<div class="card-wrap {active_class}">', unsafe_allow_html=True)
    st.markdown(f'<img class="card-img" src="data:image/png;base64,{IMG[cat]}" alt="{cat}">', unsafe_allow_html=True)
    st.markdown(f'<div class="count-badge">{count}</div>', unsafe_allow_html=True)
    if st.button(" ", key=f"card_{cat}", use_container_width=True):
        if st.session_state.selected_category == cat:
            st.session_state.selected_category = None
        else:
            st.session_state.selected_category = cat
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- Helper: render activity expanders with cost badges ---
def render_activities(cat, data):
    sort_options = {
        "Cost: Low to High": ("Cost Per Month", True),
        "Cost: High to Low": ("Cost Per Month", False),
        "Name A–Z":          ("Activity Name", True),
    }
    sort_choice = st.selectbox("Sort by", list(sort_options.keys()),
                               key=f"sort_{cat}", label_visibility="collapsed")
    sort_col, sort_asc = sort_options[sort_choice]
    data = data.sort_values(sort_col, ascending=sort_asc)

    for _, row in data.iterrows():
        with st.expander(f"{row['Activity Name']}"):
            st.markdown(
                cost_badge(row["Cost Per Month"]) + "&nbsp;&nbsp;" + mode_badge(row["Delivery Mode"]),
                unsafe_allow_html=True
            )
            st.markdown("")
            c1, c2 = st.columns([3, 2])
            with c1:
                st.write(row["Description"])
                st.caption(f"Provider: {row['Provider']}")
            with c2:
                st.write(f"**Ages:** {row['Age Group']}")
                st.write(f"**Level:** {row['Skill Level']}")
                st.write(f"**Schedule:** {row['Days Per Week']}x/week, {row['Duration (Hours)']} hr/session")
                st.write(f"**Location:** {row['Location']}")

# --- Category rows: cards + inline dropdowns ---
card_rows = [
    ["Language", "Life Skills"],
    ["All",      "Arts"],
    ["STEM",     "Sports & Games"],
]

active = st.session_state.selected_category

def cat_count(cat):
    if cat == "All":
        return len(filtered)
    return len(filtered[filtered["Category"] == cat])

for row_cats in card_rows:
    col1, col2 = st.columns(2)
    with col1:
        render_card(row_cats[0], cat_count(row_cats[0]))
    with col2:
        render_card(row_cats[1], cat_count(row_cats[1]))

    if active in row_cats:
        st.markdown("")
        if active == "All":
            for cat in ["Language", "Life Skills", "Arts", "STEM", "Sports & Games"]:
                cat_data = filtered[filtered["Category"] == cat]
                if len(cat_data) == 0:
                    continue
                st.markdown(f"#### {ICONS[cat]} {cat}")
                render_activities(cat, cat_data)
                st.markdown("")
        else:
            cat_data = filtered[filtered["Category"] == active]
            if len(cat_data) == 0:
                st.info(f"No {active} activities match your filters.")
            else:
                st.markdown(f"#### {ICONS[active]} {active}")
                render_activities(active, cat_data)
        st.markdown("---")
