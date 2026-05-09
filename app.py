import streamlit as st
import pandas as pd

st.set_page_config(page_title="Afterschool Enrichment", layout="centered")

st.markdown("## Afterschool Enrichment Activities")
st.caption("Browse online programs by category and compare costs.")

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

# --- Category Config ---
CATEGORIES = {
    "STEM":           "🔬",
    "Arts":           "🎨",
    "Language":       "🗣️",
    "Life Skills":    "💡",
    "Sports & Games": "🎮",
}

# --- Session state for selected category ---
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"

# --- Clickable Category Cards ---
st.markdown("#### Browse by Category")
cols = st.columns(len(CATEGORIES) + 1)

with cols[0]:
    if st.button("✦\nAll", use_container_width=True):
        st.session_state.selected_category = "All"

for i, (category, icon) in enumerate(CATEGORIES.items()):
    count = len(filtered[filtered["Category"] == category])
    with cols[i + 1]:
        if st.button(f"{icon}\n{category}\n({count})", use_container_width=True, disabled=(count == 0)):
            st.session_state.selected_category = category

active = st.session_state.selected_category
st.caption(f"Showing: **{active}**" if active != "All" else "Showing: **All Categories**")

st.markdown("---")

# --- Sort ---
sort_options = {
    "Cost: Low to High": ("Cost Per Month", True),
    "Cost: High to Low": ("Cost Per Month", False),
    "Name A–Z": ("Activity Name", True),
}
sort_choice = st.selectbox("Sort by", list(sort_options.keys()), label_visibility="collapsed")
sort_col, sort_asc = sort_options[sort_choice]
filtered = filtered.sort_values(sort_col, ascending=sort_asc)

# --- Activities ---
display_categories = [active] if active != "All" else list(CATEGORIES.keys())

for category in display_categories:
    cat_data = filtered[filtered["Category"] == category]
    if len(cat_data) == 0:
        continue

    icon = CATEGORIES[category]
    st.markdown(f"### {icon} {category}")

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
