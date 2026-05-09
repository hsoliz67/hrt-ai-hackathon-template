import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Afterschool Enrichment", layout="centered")

# ── Image loader ──────────────────────────────────────────────
def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

P = "data_ai/category_images/"
TITLE_IMG  = img_b64(P + "title.png")
AGE_HEADER   = img_b64(P + "age_header.png")
SKILL_HEADER = img_b64(P + "skill_header.png")

CAT_IMG = {
    "Language":       img_b64(P + "language.png"),
    "Life Skills":    img_b64(P + "life_skills.png"),
    "All":            img_b64(P + "all.png"),
    "Arts":           img_b64(P + "arts.png"),
    "STEM":           img_b64(P + "steam.png"),
    "Sports & Games": img_b64(P + "sports_games.png"),
}
CAT_ICONS = {"Language":"🗣️","Life Skills":"💡","All":"📋","Arts":"🎨","STEM":"🔬","Sports & Games":"🏆"}

AGE_IMG = {
    "Young Explorers (5–8)": img_b64(P + "age_young.png"),
    "Tweens (9–12)":         img_b64(P + "age_tweens.png"),
    "Teens (13–18)":         img_b64(P + "age_teens.png"),
}
AGE_RANGES = {"Young Explorers (5–8)":(5,8),"Tweens (9–12)":(9,12),"Teens (13–18)":(13,18)}

SKILL_IMG = {
    "Beginner":     img_b64(P + "skill_beginner.png"),
    "Intermediate": img_b64(P + "skill_intermediate.png"),
    "Advanced":     img_b64(P + "skill_advanced.png"),
}

# ── Badges ────────────────────────────────────────────────────
def cost_badge(cost):
    if cost == 0:       c, label = "#4CAF50", "FREE"
    elif cost <= 29:    c, label = "#8BC34A", f"${cost}/mo"
    elif cost <= 59:    c, label = "#FF9800", f"${cost}/mo"
    else:               c, label = "#e53935", f"${cost}/mo"
    return f'<span style="background:{c};color:white;padding:2px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">{label}</span>'

def mode_badge(mode):
    c = {"Online":"#1565C0","In-Person":"#2E7D32","Hybrid":"#6A1B9A"}.get(mode,"#555")
    return f'<span style="background:{c};color:white;padding:2px 10px;border-radius:12px;font-size:0.78rem;font-weight:700;">{mode}</span>'

# ── Styles ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&display=swap');
html, body, [class*="css"] { font-family:'Nunito',sans-serif; }
h1,h2,h3,h4 { font-family:'Nunito',sans-serif !important; font-weight:800 !important; color:#2d3a6b !important; }

.card-wrap { position:relative; width:100%; margin-bottom:4px; cursor:pointer; }
.card-wrap img.card-img { width:100%; border-radius:14px; display:block;
    transition:transform 0.15s ease, box-shadow 0.15s ease; }
.card-wrap:hover img.card-img { transform:scale(1.03); box-shadow:0 6px 20px rgba(0,0,0,0.15); }
.card-active img.card-img { box-shadow:0 0 0 4px #3d5a99 !important; border-radius:14px; }
.count-badge { position:absolute; top:8px; right:10px; background:#2d3a6b; color:white;
    font-family:'Nunito',sans-serif; font-weight:900; font-size:0.8rem;
    padding:2px 9px; border-radius:20px; z-index:5; pointer-events:none; }
.card-wrap > div[data-testid="stButton"] {
    position:absolute !important; top:0 !important; left:0 !important;
    width:100% !important; height:100% !important; z-index:10; }
.card-wrap > div[data-testid="stButton"] > button {
    width:100% !important; height:100% !important; opacity:0 !important;
    cursor:pointer !important; border:none !important; background:transparent !important; }

/* Pill buttons */
div.pill-on  > div[data-testid="stButton"] > button {
    border-radius:999px !important; font-weight:800 !important; font-family:'Nunito',sans-serif !important;
    font-size:0.85rem !important; border:2px solid #2d3a6b !important;
    background:#2d3a6b !important; color:white !important; }
div.pill-off > div[data-testid="stButton"] > button {
    border-radius:999px !important; font-weight:800 !important; font-family:'Nunito',sans-serif !important;
    font-size:0.85rem !important; border:2px solid #ccc !important;
    background:white !important; color:#2d3a6b !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────
for key, val in [("sel_category",None),("sel_age",None),("sel_skill",None),
                 ("sel_mode","All"),("favorites",set())]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Title ─────────────────────────────────────────────────────
st.markdown(
    f'<img src="data:image/png;base64,{TITLE_IMG}" style="width:100%;max-width:680px;display:block;margin:0 auto 8px auto;">',
    unsafe_allow_html=True)

df = pd.read_csv("data_ai/afterschool_activities.csv")

# ── Search row ────────────────────────────────────────────────
col_s, col_fav = st.columns([5, 1])
with col_s:
    search = st.text_input("🔍 Search activities", placeholder="e.g. Coding, Chess, SEL...", label_visibility="collapsed")
with col_fav:
    show_favs = st.toggle("❤️", help="Show saved favorites only")

# ── Delivery mode pills ───────────────────────────────────────
st.caption("Delivery Mode")
p1, p2, p3, p4, _ = st.columns([1, 1, 1, 1, 2])
for col, mode in zip([p1, p2, p3, p4], ["All", "Online", "In-Person", "Hybrid"]):
    css = "pill-on" if st.session_state.sel_mode == mode else "pill-off"
    with col:
        st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
        if st.button(mode, key=f"pill_{mode}"):
            st.session_state.sel_mode = mode
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── Location + Cost ───────────────────────────────────────────
col_loc, col_cost = st.columns([1, 2])
with col_loc:
    locations = ["All Locations"] + sorted(df["Location"].unique().tolist())
    selected_location = st.selectbox("Location", locations, label_visibility="collapsed")
with col_cost:
    mn, mx = int(df["Cost Per Month"].min()), int(df["Cost Per Month"].max())
    cost_range = st.slider("Cost", mn, mx, (mn, mx), label_visibility="collapsed")

# ── More Filters expander ─────────────────────────────────────
with st.expander("⚙️ More Filters — Age Group & Skill Level"):
    st.markdown(
        f'<img src="data:image/png;base64,{AGE_HEADER}" style="width:45%;max-width:260px;display:block;margin:8px auto 8px auto;">',
        unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)
    def age_card(label, col):
        with col:
            css = "card-active" if st.session_state.sel_age == label else ""
            st.markdown(f'<div class="card-wrap {css}">', unsafe_allow_html=True)
            st.markdown(f'<img class="card-img" src="data:image/png;base64,{AGE_IMG[label]}" alt="{label}">', unsafe_allow_html=True)
            if st.button(" ", key=f"age_{label}", use_container_width=True):
                st.session_state.sel_age = None if st.session_state.sel_age == label else label
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    age_card("Young Explorers (5–8)", a1)
    age_card("Tweens (9–12)", a2)
    age_card("Teens (13–18)", a3)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f'<img src="data:image/png;base64,{SKILL_HEADER}" style="width:45%;max-width:260px;display:block;margin:8px auto 8px auto;">',
        unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    def skill_card(label, col):
        with col:
            css = "card-active" if st.session_state.sel_skill == label else ""
            st.markdown(f'<div class="card-wrap {css}">', unsafe_allow_html=True)
            st.markdown(f'<img class="card-img" src="data:image/png;base64,{SKILL_IMG[label]}" alt="{label}">', unsafe_allow_html=True)
            if st.button(" ", key=f"skill_{label}", use_container_width=True):
                st.session_state.sel_skill = None if st.session_state.sel_skill == label else label
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    skill_card("Beginner", s1)
    skill_card("Intermediate", s2)
    skill_card("Advanced", s3)

    if st.session_state.sel_age or st.session_state.sel_skill:
        if st.button("✕ Clear Age & Skill Filters"):
            st.session_state.sel_age = None
            st.session_state.sel_skill = None
            st.rerun()

st.markdown("---")

# ── Apply filters ─────────────────────────────────────────────
def parse_age(a):
    try: p = a.strip().split("-"); return int(p[0]), int(p[1])
    except: return 0, 18

filtered = df.copy()
if search:
    filtered = filtered[filtered["Activity Name"].str.contains(search, case=False, na=False)]
if st.session_state.sel_mode != "All":
    filtered = filtered[filtered["Delivery Mode"] == st.session_state.sel_mode]
if selected_location != "All Locations":
    filtered = filtered[filtered["Location"] == selected_location]
filtered = filtered[(filtered["Cost Per Month"] >= cost_range[0]) & (filtered["Cost Per Month"] <= cost_range[1])]
if st.session_state.sel_age:
    gmin, gmax = AGE_RANGES[st.session_state.sel_age]
    filtered = filtered[filtered["Age Group"].apply(lambda a: parse_age(a)[0] <= gmax and parse_age(a)[1] >= gmin)]
if st.session_state.sel_skill:
    filtered = filtered[filtered["Skill Level"] == st.session_state.sel_skill]
if show_favs:
    filtered = filtered[filtered["Activity Name"].isin(st.session_state.favorites)]

# ── Download ──────────────────────────────────────────────────
st.download_button("⬇️ Download Results (CSV)", data=filtered.to_csv(index=False).encode(),
                   file_name="enrichment_activities.csv", mime="text/csv")

if len(filtered) == 0:
    st.info("No activities match your filters." if not show_favs else "No favorites yet — open any activity and click 'Save to Favorites'.")
    st.stop()

# ── Category cards ────────────────────────────────────────────
def cat_count(cat):
    return len(filtered) if cat == "All" else len(filtered[filtered["Category"] == cat])

def render_cat_card(cat):
    css = "card-active" if st.session_state.sel_category == cat else ""
    st.markdown(f'<div class="card-wrap {css}">', unsafe_allow_html=True)
    st.markdown(f'<img class="card-img" src="data:image/png;base64,{CAT_IMG[cat]}" alt="{cat}">', unsafe_allow_html=True)
    st.markdown(f'<div class="count-badge">{cat_count(cat)}</div>', unsafe_allow_html=True)
    if st.button(" ", key=f"cat_{cat}", use_container_width=True):
        st.session_state.sel_category = None if st.session_state.sel_category == cat else cat
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_activities(cat, data):
    opts = {"Cost: Low to High":("Cost Per Month",True),"Cost: High to Low":("Cost Per Month",False),"Name A–Z":("Activity Name",True)}
    sc, sa = opts[st.selectbox("Sort", list(opts.keys()), key=f"sort_{cat}", label_visibility="collapsed")]
    data = data.sort_values(sc, ascending=sa)
    for _, row in data.iterrows():
        is_fav = row["Activity Name"] in st.session_state.favorites
        with st.expander(f"{'♥' if is_fav else '♡'}  {row['Activity Name']}"):
            st.markdown(cost_badge(row["Cost Per Month"]) + "&nbsp;&nbsp;" + mode_badge(row["Delivery Mode"]), unsafe_allow_html=True)
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
            if st.button(f"{'Remove from' if is_fav else 'Save to'} Favorites", key=f"fav_{cat}_{row['Activity Name']}"):
                st.session_state.favorites.discard(row["Activity Name"]) if is_fav else st.session_state.favorites.add(row["Activity Name"])
                st.rerun()

card_rows = [["Language","Life Skills"],["All","Arts"],["STEM","Sports & Games"]]
active_cat = st.session_state.sel_category

for row_cats in card_rows:
    c1, c2 = st.columns(2)
    with c1: render_cat_card(row_cats[0])
    with c2: render_cat_card(row_cats[1])
    if active_cat in row_cats:
        st.markdown("")
        if active_cat == "All":
            for cat in ["Language","Life Skills","Arts","STEM","Sports & Games"]:
                d = filtered[filtered["Category"] == cat]
                if len(d) == 0: continue
                st.markdown(f"#### {CAT_ICONS[cat]} {cat}")
                render_activities(cat, d)
                st.markdown("")
        else:
            d = filtered[filtered["Category"] == active_cat]
            if len(d) == 0:
                st.info(f"No {active_cat} activities match your filters.")
            else:
                st.markdown(f"#### {CAT_ICONS[active_cat]} {active_cat}")
                render_activities(active_cat, d)
        st.markdown("---")
