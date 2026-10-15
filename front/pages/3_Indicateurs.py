"""Écran Indicateurs.

À compléter : trois st.metric et trois tableaux issus des trois endpoints
/indicateurs. Aucun graphique.
"""
from datetime import date

import pandas as pd
import streamlit as st

import api_client
import commun

st.title("Indicateurs")
commun.afficher_session()

if not commun.est_connecte():
    st.info("Veuillez vous connecter")
    st.page_link("app.py", label="Aller à la connexion")
    st.stop()

with st.form("filtres_indicateurs"):
    date_debut = st.date_input("Date de début", value=date(2026, 8, 24))
    date_fin = st.date_input("Date de fin", value=date(2026, 8, 30))
    limite = st.number_input(
        "Nombre de stations",
        min_value=1,
        max_value=50,
        value=10,
        step=1)
    actualiser = st.form_submit_button("Actualiser")

if not actualiser:
    st.info("Choisissez les critères puis cliquez sur Actualiser.")
    st.stop()

if date_debut > date_fin:
    st.error("La date de début doit être antérieure ou égale à la date de fin.")
    st.stop()

try:
    with st.spinner("Chargement..."):
        activite = api_client.obtenir("/indicateurs/activite-par-jour",
                                        params={
                                            "date_debut": date_debut.isoformat(),
                                            "date_fin": date_fin.isoformat()})

        stations = api_client.obtenir("/indicateurs/stations-actives", params={"limite": limite})

        incidents = api_client.obtenir("/indicateurs/incidents-par-statut")

except api_client.ErreurApi as erreur:
    st.error(erreur.message)
    st.stop()

nombre_trajets = 0
for jour in activite["donnees"]:
    nombre_trajets += jour["nb_trajets"]

nombre_stations = len(stations["donnees"])
delai = incidents["delai_moyen_resolution_heures"]

colonne1, colonne2, colonne3 = st.columns(3)
with colonne1:
    st.metric("Trajets sur la période", nombre_trajets)
with colonne2:
    st.metric("Stations actives", nombre_stations)
with colonne3:
    if delai is None:
        st.metric("Délai moyen de résolution (h)", "non disponible")
    else:
        st.metric("Délai moyen de résolution (h)", delai)


st.header("Activité par jour")

if not activite["donnees"]:
    st.info("Aucun résultat pour ces critères.")
else:
    tableau_activite = pd.DataFrame(activite["donnees"])
    tableau_activite = tableau_activite.rename(columns={
        "jour": "Jour",
        "nb_trajets": "Nombre de trajets"})
    st.dataframe(tableau_activite, hide_index=True)

st.header("Stations les plus actives")

if not stations["donnees"]:
    st.info("Aucun résultat pour ces critères.")
else:
    tableau_stations = pd.DataFrame(stations["donnees"])
    tableau_stations["Total"] = (tableau_stations["nb_departs"] + tableau_stations["nb_arrivees"])
    tableau_stations = tableau_stations.rename(columns={
        "station_id": "Identifiant",
        "nom": "Nom",
        "nb_departs": "Départs",
        "nb_arrivees": "Arrivées"})
    st.dataframe(tableau_stations, hide_index=True)

st.header("Incidents par statut")

if not incidents["donnees"]:
    st.info("Aucun résultat pour ces critères.")
else:
    tableau_incidents = pd.DataFrame(incidents["donnees"])
    tableau_incidents = tableau_incidents.rename(columns={
        "statut": "Statut",
        "nb_incidents": "Nombre d'incidents"})
    st.dataframe(tableau_incidents, hide_index=True)