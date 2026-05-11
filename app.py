import streamlit as st
import pandas as pd
import base64

st.set_page_config(page_title="Afterschool Enrichment", layout="centered")

# ── Image loader ──────────────────────────────────────────────
def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

P = "data_ai/category_images/"
TITLE_IMG    = img_b64(P + "title.png")
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

# ── Translations ───────────────────────────────────────────────
TRANSLATIONS = {
    "English": {
        "tagline": "Compare, Save, and Discover: The smarter way to find enrichment.",
        "mission": "Our mission is to bridge the gap between families and opportunity. By centralizing out-of-school programs and providing transparent cost comparisons, we empower every child to explore their passions, regardless of their schedule or budget.",
        "search_placeholder": "e.g. Coding, Chess, SEL...",
        "show_favorites": "Show saved favorites only",
        "delivery_mode": "Delivery Mode",
        "modes": {"All": "All", "Online": "Online", "In-Person": "In-Person", "Hybrid": "Hybrid"},
        "all_locations": "All Locations",
        "more_filters": "⚙️ More Filters — Age Group & Skill Level",
        "clear_age_skill": "✕ Clear Age & Skill Filters",
        "download": "⬇️ Download Results (CSV)",
        "no_match": "No activities match your filters.",
        "no_favorites": "No favorites yet — open any activity and click 'Save to Favorites'.",
        "col_activity": "ACTIVITY",
        "col_cost": "COST",
        "col_mode": "MODE",
        "col_ages": "AGES",
        "sort_low_high": "Cost: Low to High",
        "sort_high_low": "Cost: High to Low",
        "sort_az": "Name A–Z",
        "provider": "Provider",
        "level": "Level",
        "schedule": "Schedule",
        "location": "Location",
        "save_fav": "♡ Save to Favorites",
        "remove_fav": "♥ Remove from Favorites",
        "compare_title": "Compare Programs",
        "compare_info": "Select at least 2 programs using the ⊕ button to compare them.",
        "clear_compare": "✕ Clear Comparison",
        "suggest_title": "💡 Don't see what you're looking for?",
        "suggest_subtitle": "Suggest a program and we'll look into adding it!",
        "suggest_program_name": "Program Name *",
        "suggest_program_placeholder": "e.g. Robotics Club",
        "suggest_category": "Category *",
        "suggest_age": "Age Group *",
        "suggest_mode": "Delivery Mode",
        "suggest_skill": "Skill Level",
        "suggest_your_name": "Your Name (optional)",
        "suggest_your_name_placeholder": "First name only is fine",
        "suggest_desc": "Why would this program be valuable?",
        "suggest_desc_placeholder": "Tell us a bit about it — who it's for, what kids would learn, etc.",
        "suggest_submit": "📨 Submit Suggestion",
        "suggest_warning": "Please enter a program name before submitting.",
        "suggest_success": "Thank you! Your suggestion for **{name}** has been submitted. We appreciate your input! 🎉",
        "not_sure": "Not Sure",
        "all_levels": "All Levels",
        "all_ages": "All Ages",
        "week_schedule": "{days}x/week · {hours} hr/session",
        "days_per_week": "Days/Week",
        "hours_session": "Hours/Session",
        "ages_label": "Ages",
        "mode_label": "Mode",
        "category_label": "Category",
        "cost_month": "Cost/Month",
        "no_activities_cat": "No {cat} activities match your filters.",
        "selected_label": "selected",
    },
    "Español": {
        "tagline": "Compara, Guarda y Descubre: La forma más inteligente de encontrar enriquecimiento.",
        "mission": "Nuestra misión es cerrar la brecha entre las familias y las oportunidades. Al centralizar los programas extraescolares y proporcionar comparaciones de costos transparentes, empoderamos a cada niño para explorar sus pasiones, sin importar su horario o presupuesto.",
        "search_placeholder": "ej. Programación, Ajedrez, SEL...",
        "show_favorites": "Mostrar solo favoritos guardados",
        "delivery_mode": "Modalidad",
        "modes": {"All": "Todos", "Online": "En Línea", "In-Person": "Presencial", "Hybrid": "Híbrido"},
        "all_locations": "Todas las Ubicaciones",
        "more_filters": "⚙️ Más Filtros — Grupo de Edad y Nivel",
        "clear_age_skill": "✕ Borrar Filtros de Edad y Nivel",
        "download": "⬇️ Descargar Resultados (CSV)",
        "no_match": "Ninguna actividad coincide con tus filtros.",
        "no_favorites": "Aún no hay favoritos — abre una actividad y haz clic en 'Guardar en Favoritos'.",
        "col_activity": "ACTIVIDAD",
        "col_cost": "COSTO",
        "col_mode": "MODO",
        "col_ages": "EDADES",
        "sort_low_high": "Costo: Menor a Mayor",
        "sort_high_low": "Costo: Mayor a Menor",
        "sort_az": "Nombre A–Z",
        "provider": "Proveedor",
        "level": "Nivel",
        "schedule": "Horario",
        "location": "Ubicación",
        "save_fav": "♡ Guardar en Favoritos",
        "remove_fav": "♥ Quitar de Favoritos",
        "compare_title": "Comparar Programas",
        "compare_info": "Selecciona al menos 2 programas con el botón ⊕ para compararlos.",
        "clear_compare": "✕ Borrar Comparación",
        "suggest_title": "💡 ¿No encuentras lo que buscas?",
        "suggest_subtitle": "¡Sugiere un programa y lo consideraremos para agregar!",
        "suggest_program_name": "Nombre del Programa *",
        "suggest_program_placeholder": "ej. Club de Robótica",
        "suggest_category": "Categoría *",
        "suggest_age": "Grupo de Edad *",
        "suggest_mode": "Modalidad",
        "suggest_skill": "Nivel de Habilidad",
        "suggest_your_name": "Tu Nombre (opcional)",
        "suggest_your_name_placeholder": "Solo el primer nombre está bien",
        "suggest_desc": "¿Por qué sería valioso este programa?",
        "suggest_desc_placeholder": "Cuéntanos un poco — para quién es, qué aprenderían los niños, etc.",
        "suggest_submit": "📨 Enviar Sugerencia",
        "suggest_warning": "Por favor ingresa el nombre del programa antes de enviar.",
        "suggest_success": "¡Gracias! Tu sugerencia para **{name}** ha sido enviada. ¡Apreciamos tu aporte! 🎉",
        "not_sure": "No estoy seguro/a",
        "all_levels": "Todos los Niveles",
        "all_ages": "Todas las Edades",
        "week_schedule": "{days}x/semana · {hours} hr/sesión",
        "days_per_week": "Días/Semana",
        "hours_session": "Horas/Sesión",
        "ages_label": "Edades",
        "mode_label": "Modo",
        "category_label": "Categoría",
        "cost_month": "Costo/Mes",
        "no_activities_cat": "No hay actividades de {cat} que coincidan con tus filtros.",
        "selected_label": "seleccionados",
    }
}

def t(key, **kwargs):
    lang = st.session_state.get("sel_lang", "English")
    val = TRANSLATIONS[lang].get(key, TRANSLATIONS["English"].get(key, key))
    return val.format(**kwargs) if kwargs and isinstance(val, str) else val

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
                 ("sel_mode","All"),("favorites",set()),("compare_set",set()),
                 ("sel_lang","English")]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Language selector ─────────────────────────────────────────
lang_col, spacer = st.columns([1, 5])
with lang_col:
    lang_options = list(TRANSLATIONS.keys())
    new_lang = st.selectbox("🌐", lang_options,
                            index=lang_options.index(st.session_state.sel_lang),
                            label_visibility="collapsed")
    if new_lang != st.session_state.sel_lang:
        st.session_state.sel_lang = new_lang
        st.rerun()

# ── Title ─────────────────────────────────────────────────────
st.markdown(
    f'<img src="data:image/png;base64,{TITLE_IMG}" style="width:100%;max-width:680px;display:block;margin:0 auto 8px auto;">',
    unsafe_allow_html=True)

st.markdown(
    f'<p style="text-align:center;font-size:1.05rem;font-weight:800;color:#3d5a99;margin:4px 0 2px 0;">{t("tagline")}</p>',
    unsafe_allow_html=True)
with st.expander("📖 Our Mission"):
    st.markdown(
        f'<p style="font-size:0.95rem;color:#444;line-height:1.6;">{t("mission")}</p>',
        unsafe_allow_html=True)

df = pd.read_csv("data_ai/afterschool_activities.csv")

# ── Search row ────────────────────────────────────────────────
col_s, col_fav = st.columns([5, 1])
with col_s:
    search = st.text_input("🔍", placeholder=t("search_placeholder"), label_visibility="collapsed")
with col_fav:
    show_favs = st.toggle("❤️", help=t("show_favorites"))

# ── Delivery mode pills ───────────────────────────────────────
st.caption(t("delivery_mode"))
mode_keys = ["All", "Online", "In-Person", "Hybrid"]
p1, p2, p3, p4, _ = st.columns([1, 1, 1, 1, 2])
for col, mode in zip([p1, p2, p3, p4], mode_keys):
    label = t("modes")[mode]
    css = "pill-on" if st.session_state.sel_mode == mode else "pill-off"
    with col:
        st.markdown(f'<div class="{css}">', unsafe_allow_html=True)
        if st.button(label, key=f"pill_{mode}"):
            st.session_state.sel_mode = mode
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── Location + Cost ───────────────────────────────────────────
col_loc, col_cost = st.columns([1, 2])
with col_loc:
    locations = [t("all_locations")] + sorted(df["Location"].unique().tolist())
    selected_location = st.selectbox("Location", locations, label_visibility="collapsed")
with col_cost:
    mn, mx = int(df["Cost Per Month"].min()), int(df["Cost Per Month"].max())
    cost_range = st.slider("Cost", mn, mx, (mn, mx), label_visibility="collapsed")

# ── More Filters expander ─────────────────────────────────────
with st.expander(t("more_filters")):
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
        if st.button(t("clear_age_skill")):
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
if selected_location != t("all_locations"):
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
st.download_button(t("download"), data=filtered.to_csv(index=False).encode(),
                   file_name="enrichment_activities.csv", mime="text/csv")

if len(filtered) == 0:
    st.info(t("no_match") if not show_favs else t("no_favorites"))
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
    sort_options = {
        t("sort_low_high"): ("Cost Per Month", True),
        t("sort_high_low"): ("Cost Per Month", False),
        t("sort_az"):       ("Activity Name", True),
    }
    selected_sort = st.selectbox("Sort", list(sort_options.keys()), key=f"sort_{cat}", label_visibility="collapsed")
    sc, sa = sort_options[selected_sort]
    data = data.sort_values(sc, ascending=sa)

    if "open_detail" not in st.session_state:
        st.session_state.open_detail = {}

    h1, h2, h3, h4, h5, h6 = st.columns([3, 1.2, 1, 1, 0.6, 0.6])
    h1.markdown(f"<span style='font-size:0.78rem;color:#888;font-weight:700;'>{t('col_activity')}</span>", unsafe_allow_html=True)
    h2.markdown(f"<span style='font-size:0.78rem;color:#888;font-weight:700;'>{t('col_cost')}</span>", unsafe_allow_html=True)
    h3.markdown(f"<span style='font-size:0.78rem;color:#888;font-weight:700;'>{t('col_mode')}</span>", unsafe_allow_html=True)
    h4.markdown(f"<span style='font-size:0.78rem;color:#888;font-weight:700;'>{t('col_ages')}</span>", unsafe_allow_html=True)
    h5.markdown("<span style='font-size:0.78rem;color:#888;font-weight:700;'></span>", unsafe_allow_html=True)
    h6.markdown("<span style='font-size:0.78rem;color:#888;font-weight:700;'>CMP</span>", unsafe_allow_html=True)
    st.markdown("<hr style='margin:4px 0 8px 0;border-color:#eee;'>", unsafe_allow_html=True)

    for _, row in data.iterrows():
        uid = f"{cat}__{row['Activity Name']}"
        is_open = st.session_state.open_detail.get(uid, False)
        is_fav = row["Activity Name"] in st.session_state.favorites
        in_compare = row["Activity Name"] in st.session_state.compare_set

        c1, c2, c3, c4, c5, c6 = st.columns([3, 1.2, 1, 1, 0.6, 0.6])
        with c1:
            fav_icon = "♥ " if is_fav else ""
            st.markdown(f"**{fav_icon}{row['Activity Name']}**")
        with c2:
            st.markdown(cost_badge(row["Cost Per Month"]), unsafe_allow_html=True)
        with c3:
            st.markdown(mode_badge(row["Delivery Mode"]), unsafe_allow_html=True)
        with c4:
            st.markdown(f"<span style='font-size:0.85rem;color:#444;'>{row['Age Group']}</span>", unsafe_allow_html=True)
        with c6:
            cmp_label = "⊖" if in_compare else "⊕"
            if st.button(cmp_label, key=f"cmp_{uid}", help="Add/remove from comparison"):
                if in_compare:
                    st.session_state.compare_set.discard(row["Activity Name"])
                else:
                    st.session_state.compare_set.add(row["Activity Name"])
                st.rerun()
        with c5:
            if st.button("▾" if is_open else "▸", key=f"tog_{uid}"):
                st.session_state.open_detail[uid] = not is_open
                st.rerun()

        if is_open:
            with st.container():
                st.markdown(
                    "<div style='background:#f8f9fb;border-radius:10px;padding:14px 18px;margin:4px 0 10px 0;'>",
                    unsafe_allow_html=True)
                d1, d2 = st.columns([3, 2])
                with d1:
                    st.write(row["Description"])
                    st.caption(f"{t('provider')}: {row['Provider']}")
                with d2:
                    st.write(f"**{t('level')}:** {row['Skill Level']}")
                    st.write(f"**{t('schedule')}:** " + t("week_schedule", days=row['Days Per Week'], hours=row['Duration (Hours)']))
                    st.write(f"**{t('location')}:** {row['Location']}")
                fav_label = t("remove_fav") if is_fav else t("save_fav")
                if st.button(fav_label, key=f"fav_{uid}"):
                    st.session_state.favorites.discard(row["Activity Name"]) if is_fav else st.session_state.favorites.add(row["Activity Name"])
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<hr style='margin:2px 0;border-color:#f0f0f0;'>", unsafe_allow_html=True)

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
                st.info(t("no_activities_cat", cat=active_cat))
            else:
                st.markdown(f"#### {CAT_ICONS[active_cat]} {active_cat}")
                render_activities(active_cat, d)
        st.markdown("---")

# ── Compare Panel ─────────────────────────────────────────────
if st.session_state.compare_set:
    st.markdown("---")
    cmp_names = list(st.session_state.compare_set)
    st.markdown(f"### ⚖️ {t('compare_title')} ({len(cmp_names)} {t('selected_label')})")
    if len(cmp_names) < 2:
        st.info(t("compare_info"))
    else:
        cmp_df = df[df["Activity Name"].isin(cmp_names)].set_index("Activity Name")
        display_fields = [
            ("Category",         t("category_label")),
            ("Cost Per Month",   t("cost_month")),
            ("Delivery Mode",    t("mode_label")),
            ("Age Group",        t("ages_label")),
            ("Skill Level",      t("level")),
            ("Days Per Week",    t("days_per_week")),
            ("Duration (Hours)", t("hours_session")),
            ("Location",         t("location")),
            ("Provider",         t("provider")),
        ]
        cols = st.columns(len(cmp_names))
        for col, name in zip(cols, cmp_names):
            row = cmp_df.loc[name]
            with col:
                st.markdown(f"**{name}**")
                st.markdown(cost_badge(row["Cost Per Month"]), unsafe_allow_html=True)
                st.markdown(mode_badge(row["Delivery Mode"]), unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                for field, label in display_fields[2:]:
                    st.markdown(f"<span style='font-size:0.78rem;color:#888;font-weight:700;'>{label.upper()}</span><br>"
                                f"<span style='font-size:0.9rem;'>{row[field]}</span>", unsafe_allow_html=True)
                    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
                st.caption(row.get("Description", "")[:120] + "..." if len(str(row.get("Description",""))) > 120 else row.get("Description",""))
    if st.button(t("clear_compare")):
        st.session_state.compare_set = set()
        st.rerun()

# ── Suggest a Program ─────────────────────────────────────────
st.markdown("---")
st.markdown(f"### {t('suggest_title')}")
st.markdown(t("suggest_subtitle"))

SUGGESTIONS_FILE = "data_ai/suggestions.csv"

with st.form("suggest_form", clear_on_submit=True):
    s1, s2 = st.columns(2)
    with s1:
        sug_name = st.text_input(t("suggest_program_name"), placeholder=t("suggest_program_placeholder"))
        sug_category = st.selectbox(t("suggest_category"), ["Language", "Life Skills", "Arts", "STEM", "Sports & Games", "Other"])
        sug_age = st.selectbox(t("suggest_age"), ["Young Explorers (5–8)", "Tweens (9–12)", "Teens (13–18)", t("all_ages")])
    with s2:
        sug_mode = st.selectbox(t("suggest_mode"), ["In-Person", "Online", "Hybrid", t("not_sure")])
        sug_skill = st.selectbox(t("suggest_skill"), ["Beginner", "Intermediate", "Advanced", t("all_levels")])
        sug_name_field = st.text_input(t("suggest_your_name"), placeholder=t("suggest_your_name_placeholder"))
    sug_desc = st.text_area(t("suggest_desc"), placeholder=t("suggest_desc_placeholder"), height=100)
    submitted = st.form_submit_button(t("suggest_submit"), use_container_width=True)

if submitted:
    if not sug_name.strip():
        st.warning(t("suggest_warning"))
    else:
        import os, datetime
        new_row = pd.DataFrame([{
            "Program Name":  sug_name.strip(),
            "Category":      sug_category,
            "Age Group":     sug_age,
            "Delivery Mode": sug_mode,
            "Skill Level":   sug_skill,
            "Description":   sug_desc.strip(),
            "Submitted By":  sug_name_field.strip(),
            "Submitted At":  datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }])
        if os.path.exists(SUGGESTIONS_FILE):
            existing = pd.read_csv(SUGGESTIONS_FILE)
            pd.concat([existing, new_row], ignore_index=True).to_csv(SUGGESTIONS_FILE, index=False)
        else:
            new_row.to_csv(SUGGESTIONS_FILE, index=False)
        st.success(t("suggest_success", name=sug_name.strip()))
