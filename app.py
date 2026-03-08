import streamlit as st
import requests
import csv
import io
import time

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
SPREADSHEET_ID = "1SHAZ_aYKYEW2llawuNSX5iUf0f7JK__UztYod4GLfOo"
SHEET_NAME = "Feuil1"
PASSWORD = "JOGO2026"

# URL du Google Apps Script (renseignée via st.secrets sur Streamlit Cloud)
APPS_SCRIPT_URL = st.secrets.get("APPS_SCRIPT_URL", "")

# Dates de l'événement
DATES = [
    "Vendredi 10 juillet",
    "Samedi 11 juillet",
    "Dimanche 12 juillet",
    "Lundi 13 juillet",
    "Mardi 14 juillet",
    "Mercredi 15 juillet",
]

# ─────────────────────────────────────────────────────────────────────────────
# MAPPING PRÉCIS : correspondance entre les lignes CSV (0-based) et les lignes
# Google Sheets (1-based, pour l'écriture via Apps Script)
#
# Structure du CSV (17 lignes, 0-based) :
#  0  : en-tête DISPONIBILITE
#  1  : dates
#  2  : dispo place 1  → GS row 3
#  3  : dispo place 2  → GS row 4
#  4  : dispo place 3  → GS row 5
#  5  : dispo place 4  → GS row 6
#  6  : dispo place 5  → GS row 7
#  7  : dispo place 6  → GS row 8
#  8  : dispo place 7  → GS row 9
#  9  : dispo place 8  → GS row 10
# 10  : en-tête COUCHAGES (ligne 11 GS = ligne vide, mais le CSV la compresse)
# 11  : dates couchages → GS row 13
# 12  : Chambre 1 Lit 1 → GS row 14
# 13  : Chambre 1 Lit 2 → GS row 15
# 14  : Chambre 2 Lit 1 → GS row 16
# 15  : Chambre 2 Lit 2 → GS row 17
# 16  : Canapé          → GS row 18
# ─────────────────────────────────────────────────────────────────────────────

# Disponibilité générale : lignes CSV 2 à 9 → GS rows 3 à 10
DISPO_GENERAL = [
    {"csv_row": 2, "gs_row": 3, "label": "Place 1", "vendredi_ok": True},
    {"csv_row": 3, "gs_row": 4, "label": "Place 2", "vendredi_ok": True},
    {"csv_row": 4, "gs_row": 5, "label": "Place 3", "vendredi_ok": True},
    {"csv_row": 5, "gs_row": 6, "label": "Place 4", "vendredi_ok": True},
    {"csv_row": 6, "gs_row": 7, "label": "Place 5", "vendredi_ok": False},
    {"csv_row": 7, "gs_row": 8, "label": "Place 6", "vendredi_ok": False},
    {"csv_row": 8, "gs_row": 9, "label": "Place 7", "vendredi_ok": False},
    {"csv_row": 9, "gs_row": 10, "label": "Place 8", "vendredi_ok": False},
]

# Couchages : lignes CSV 12 à 16 → GS rows 14 à 18
COUCHAGES = [
    {"csv_row": 12, "gs_row": 14, "label": "Chambre 1 — Lit 1"},
    {"csv_row": 13, "gs_row": 15, "label": "Chambre 1 — Lit 2"},
    {"csv_row": 14, "gs_row": 16, "label": "Chambre 2 — Lit 1"},
    {"csv_row": 15, "gs_row": 17, "label": "Chambre 2 — Lit 2"},
    {"csv_row": 16, "gs_row": 18, "label": "Canapé"},
]

# Colonnes CSV (0-based) et GSheets (1-based) pour chaque date
DATE_CSV_COL = {date: i + 1 for i, date in enumerate(DATES)}   # col CSV 1-6
DATE_GS_COL  = {date: i + 2 for i, date in enumerate(DATES)}   # col GS 2-7

# ─────────────────────────────────────────────
# LECTURE DU SHEET (URL CSV publique)
# ─────────────────────────────────────────────
@st.cache_data(ttl=15)
def load_sheet_data():
    url = (
        f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
        f"/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
    )
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        reader = csv.reader(io.StringIO(r.text))
        return list(reader)
    except Exception as e:
        st.error(f"Impossible de charger les données : {e}")
        return []

def get_cell(rows, csv_row_0based, csv_col_0based):
    """Retourne la valeur d'une cellule (index 0-based)."""
    try:
        return rows[csv_row_0based][csv_col_0based].strip()
    except IndexError:
        return ""

# ─────────────────────────────────────────────
# ÉCRITURE DANS LE SHEET (via Apps Script)
# ─────────────────────────────────────────────
def write_cell(gs_row, gs_col, value):
    if not APPS_SCRIPT_URL:
        st.error(
            "⚠️ L'URL du script n'est pas encore configurée. "
            "Suivez le guide de déploiement joint pour finaliser l'installation."
        )
        return False, "URL manquante"
    try:
        payload = {"row": gs_row, "col": gs_col, "value": value}
        r = requests.post(APPS_SCRIPT_URL, json=payload, timeout=15)
        result = r.json()
        return result.get("success", False), result.get("message", "")
    except Exception as e:
        return False, str(e)

# ─────────────────────────────────────────────
# PAGE D'ACCUEIL — MOT DE PASSE
# ─────────────────────────────────────────────
def show_login():
    st.markdown(
        """
        <div style='text-align:center; padding: 3rem 1rem 1rem 1rem;'>
            <h1 style='font-size:2.8rem; color:#2c3e50;'>🎉 CHEZ JOGO</h1>
            <h3 style='color:#7f8c8d; font-weight:400;'>Anniversaire · Juillet 2026</h3>
            <p style='color:#95a5a6; margin-top:0.5rem;'>10 au 15 juillet</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("---")
        pwd = st.text_input(
            "Mot de passe",
            type="password",
            placeholder="Entrez le mot de passe...",
            label_visibility="collapsed",
        )
        if st.button("Accéder aux réservations", use_container_width=True, type="primary"):
            if pwd == PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Mot de passe incorrect.")
        st.markdown(
            "<p style='text-align:center; color:#bdc3c7; font-size:0.8rem; margin-top:1rem;'>"
            "Accès réservé aux invités</p>",
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────
# FORMULAIRE DE RÉSERVATION
# ─────────────────────────────────────────────
def show_reservation_form(section, label, date, gs_row, gs_col):
    with st.form(key=f"form_{gs_row}_{gs_col}"):
        st.markdown(f"### Réserver cette place")
        st.markdown(f"**Section :** {section}")
        st.markdown(f"**Place :** {label}")
        st.markdown(f"**Date :** {date}")
        st.markdown("---")

        prenom = st.text_input("Prénom *", placeholder="Votre prénom")
        nom = st.text_input("Nom *", placeholder="Votre nom de famille")

        col_submit, col_cancel = st.columns(2)
        submitted = col_submit.form_submit_button(
            "✅ Confirmer la réservation", use_container_width=True, type="primary"
        )
        cancelled = col_cancel.form_submit_button("Annuler", use_container_width=True)

        if submitted:
            if not prenom.strip() or not nom.strip():
                st.warning("Veuillez renseigner votre prénom et votre nom.")
            else:
                display_name = f"{prenom.strip()} {nom.strip()}"
                success, message = write_cell(gs_row, gs_col, display_name)
                if success:
                    st.success(f"🎉 Réservation confirmée pour {prenom} {nom} !")
                    st.cache_data.clear()
                    time.sleep(1.5)
                    st.session_state["active_form"] = None
                    st.rerun()
                else:
                    st.error(f"Erreur lors de la réservation : {message}")

        if cancelled:
            st.session_state["active_form"] = None
            st.rerun()

# ─────────────────────────────────────────────
# BOUTON DE CELLULE
# ─────────────────────────────────────────────
def cell_button(rows, section, label, date, csv_row, gs_row, gs_col):
    csv_col = DATE_CSV_COL[date]
    value = get_cell(rows, csv_row, csv_col)
    key = f"btn_{gs_row}_{gs_col}"
    form_key = f"{gs_row}_{gs_col}"

    if value == "Libre":
        if st.button("🟢 Libre", key=key, use_container_width=True):
            st.session_state["active_form"] = form_key
            st.session_state["form_params"] = {
                "section": section,
                "label": label,
                "date": date,
                "gs_row": gs_row,
                "gs_col": gs_col,
            }
            st.rerun()
    elif value == "":
        st.button("⬜ —", key=key, disabled=True, use_container_width=True)
    else:
        st.button("🔴 Indisponible", key=key, disabled=True, use_container_width=True)

# ─────────────────────────────────────────────
# APPLICATION PRINCIPALE
# ─────────────────────────────────────────────
def show_main_app():
    st.markdown(
        """
        <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
            <h1 style='font-size:2.2rem; color:#2c3e50;'>🎉 CHEZ JOGO — Réservations</h1>
            <p style='color:#7f8c8d;'>Anniversaire · 10 au 15 juillet 2026</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_top1, col_top2 = st.columns([5, 1])
    with col_top2:
        if st.button("🔒 Déconnexion"):
            st.session_state["authenticated"] = False
            st.rerun()

    with st.spinner("Chargement des disponibilités..."):
        rows = load_sheet_data()

    if not rows:
        st.error("Impossible de charger les données. Vérifiez la connexion au Google Sheet.")
        return

    # Formulaire actif
    if st.session_state.get("active_form") and st.session_state.get("form_params"):
        p = st.session_state["form_params"]
        st.markdown("---")
        show_reservation_form(
            section=p["section"],
            label=p["label"],
            date=p["date"],
            gs_row=p["gs_row"],
            gs_col=p["gs_col"],
        )
        st.markdown("---")
        return

    # ── SECTION 1 : DISPONIBILITÉ GÉNÉRALE ──────────────────────────────────
    st.markdown("## 📅 Disponibilité générale")
    st.caption("Votre présence à l'événement par date")

    header = st.columns([1.5] + [1] * len(DATES))
    header[0].markdown("**Place**")
    for i, date in enumerate(DATES):
        header[i + 1].markdown(f"**{date}**")

    for place in DISPO_GENERAL:
        row_cols = st.columns([1.5] + [1] * len(DATES))
        row_cols[0].markdown(f"**{place['label']}**")
        for i, date in enumerate(DATES):
            gs_col = DATE_GS_COL[date]
            with row_cols[i + 1]:
                if date == "Vendredi 10 juillet" and not place["vendredi_ok"]:
                    st.button("⬜ —", key=f"na_{place['gs_row']}_{gs_col}",
                              disabled=True, use_container_width=True)
                else:
                    cell_button(
                        rows,
                        section="Disponibilité générale",
                        label=place["label"],
                        date=date,
                        csv_row=place["csv_row"],
                        gs_row=place["gs_row"],
                        gs_col=gs_col,
                    )

    st.markdown("---")

    # ── SECTION 2 : COUCHAGES ────────────────────────────────────────────────
    st.markdown("## 🛏️ Couchages")
    st.caption("Réservation des places de couchage par nuit")

    header2 = st.columns([1.5] + [1] * len(DATES))
    header2[0].markdown("**Couchage**")
    for i, date in enumerate(DATES):
        header2[i + 1].markdown(f"**{date}**")

    for couchage in COUCHAGES:
        row_cols = st.columns([1.5] + [1] * len(DATES))
        row_cols[0].markdown(f"**{couchage['label']}**")
        for i, date in enumerate(DATES):
            gs_col = DATE_GS_COL[date]
            with row_cols[i + 1]:
                cell_button(
                    rows,
                    section="Couchages",
                    label=couchage["label"],
                    date=date,
                    csv_row=couchage["csv_row"],
                    gs_row=couchage["gs_row"],
                    gs_col=gs_col,
                )

    # Légende
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align:center; color:#7f8c8d; font-size:0.85rem;'>
            🟢 <b>Libre</b> : cliquez pour réserver &nbsp;|&nbsp;
            🔴 <b>Indisponible</b> : déjà réservé &nbsp;|&nbsp;
            ⬜ <b>—</b> : non disponible ce jour
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")
    if st.button("🔄 Actualiser les disponibilités"):
        st.cache_data.clear()
        st.rerun()

# ─────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="CHEZ JOGO — Réservations",
        page_icon="🎉",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "active_form" not in st.session_state:
        st.session_state["active_form"] = None
    if "form_params" not in st.session_state:
        st.session_state["form_params"] = None

    if not st.session_state["authenticated"]:
        show_login()
    else:
        show_main_app()


if __name__ == "__main__":
    main()
