"""Écran Incidents.

À compléter : tableau filtrable par statut ; pour le rôle exploitant, changement de
statut d'un incident via l'API.
"""
import pandas as pd
import streamlit as st

import api_client
import commun

st.title("Incidents")
if "message_incident" in st.session_state:
    st.success(st.session_state.pop("message_incident"))
commun.afficher_session()

if not commun.est_connecte():
    st.info("Veuillez vous connecter")
    st.page_link("app.py", label="Aller à la connexion")
    st.stop()

with st.form("filtres_incidents"):
    statut = st.selectbox("Statut", options=["Tous", "ouvert", "en_cours", "resolu"])
    st.caption("Si vous changez de statut, revenez à la page 1.")

    taille_page = st.selectbox("Incidents par page", options=[10, 20, 50], index=1)
    page = st.number_input("Page", min_value=1, value=1, step=1)
    st.form_submit_button("Afficher")

params = {"page": page, "taille_page": taille_page}

if statut != "Tous":
    params["statut"] = statut

try:
    with st.spinner("Chargement..."):
        reponse = api_client.obtenir("/incidents", params=params)

except api_client.ErreurApi as erreur:
    st.error(erreur.message)
    st.stop()

else:
    if not reponse["resultats"]:
        st.info("Aucun résultat pour ces critères.")

    else:
        st.write(f"{reponse['total']} incidents au total")

        nombre_pages = (reponse["total"] + taille_page - 1) // taille_page
        st.caption(f"Page {page} sur {nombre_pages}")

        tableau = pd.DataFrame(reponse["resultats"])
        tableau = tableau.rename(columns={
            "incident_id": "Identifiant",
            "date_signalement": "Signalé le",
            "cible": "Cible",
            "velo_id": "Vélo",
            "station_id": "Station",
            "type_incident": "Type",
            "statut": "Statut",
            "date_resolution": "Résolu le",
            "technicien": "Technicien"})

        st.dataframe(tableau, hide_index=True)

if st.session_state["role"] == "exploitant":
    if reponse["resultats"]:
        st.header("Changer le statut d'un incident")
        identifiants = [incident["incident_id"] for incident in reponse["resultats"]]
        with st.form("modifier_statut"):
            incident_id = st.selectbox("Incident", options=identifiants)
            nouveau_statut = st.selectbox("Nouveau statut", options=["en_cours", "resolu"])
            appliquer = st.form_submit_button("Appliquer")

        if appliquer:

            try:
                with st.spinner("Modification..."):
                    api_client.modifier_statut(incident_id, nouveau_statut)

            except api_client.ErreurApi as erreur:
                if erreur.status_code == 403:
                    st.error("Vous n'avez pas le droit de modifier un incident.")
                elif erreur.status_code == 422:
                    st.error("Transition de statut non autorisée.")
                elif erreur.status_code == 404:
                    st.error("Incident introuvable.")
                else:
                    st.error(erreur.message)

            else:
                st.session_state["message_incident"] = (f"Statut de l'incident {incident_id} mis à jour : {nouveau_statut}.")
                st.rerun()

else:
    st.info("La modification des incidents est réservée aux exploitants.")