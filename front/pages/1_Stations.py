"""Écran Stations.

À compléter : tableau des stations filtrable par commune, pagination.
"""

import pandas as pd
import streamlit as st

import api_client
import commun

@st.cache_data(ttl=3600)
def charger_communes():
    """Récupère les communes distinctes des stations"""
    communes = []
    page = 1
    while True:
        reponse = api_client.obtenir("/stations", params={"page": page, "taille_page": 100})
        for station in reponse["resultats"]:

            if station["commune"] not in communes:
                communes.append(station["commune"])

        if page * 100 >= reponse["total"]:
            break

        page += 1
    return sorted(communes)

st.title("Stations")
commun.afficher_session()

if not commun.est_connecte():
    st.info("Veuillez vous connecter")
    st.page_link("app.py", label="Aller à la connexion")
    st.stop()

try:
    with st.spinner("Chargement des communes..."):
        communes = charger_communes()
except api_client.ErreurApi as erreur:
    st.error(erreur.message)
    st.stop()

with st.form("pagination_stations"):
    commune = st.selectbox("Commune", options=["Toutes"] + communes)
    st.caption("Si vous changez de commune, revenez à la page 1.")
    taille_page = st.selectbox("Stations par page", options=[10, 20, 50], index=1)
    page = st.number_input(
        "Page",
        min_value=1,
        value=1,
        step=1)
    st.form_submit_button("Afficher")

params = {"page": page, "taille_page": taille_page}
if commune != "Toutes": params["commune"] = commune

try:
    with st.spinner("Chargement..."):
        reponse = api_client.obtenir("/stations", params=params)
except api_client.ErreurApi as erreur:
    st.error(erreur.message)

else:
    if not reponse["resultats"]:
        st.info("Aucun résultat pour ces critères.")

    else:
        st.write(f"{reponse['total']} stations au total")

        nombre_pages = (reponse["total"] + taille_page - 1) // taille_page
        st.caption(f"Page {page} sur {nombre_pages}")

        tableau = pd.DataFrame(reponse["resultats"])
        tableau = tableau.rename(columns={
            "station_id": "Identifiant",
            "nom": "Nom",
            "commune": "Commune",
            "capacite": "Capacité",
            "date_mise_en_service": "Mise en service"})

        st.dataframe(
            tableau[[
                "Identifiant",
                "Nom",
                "Commune",
                "Capacité",
                "Mise en service"]],
            hide_index=True)