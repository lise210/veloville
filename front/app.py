"""Page d'accueil Streamlit : connexion.

À compléter : formulaire identifiant / mot de passe, appel de POST /auth/login via
api_client, stockage du jeton et du rôle dans st.session_state,
message d'erreur en français en cas d'échec.

Lancement : streamlit run front/app.py
"""

import streamlit as st

import api_client
import commun

st.set_page_config(page_title="VéloVille", layout="wide")
st.title("VéloVille — Plateforme de restitution")
st.header("Connexion")

if not commun.est_connecte():
    with st.form("connexion", clear_on_submit=True):
        identifiant = st.text_input("Identifiant")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        soumettre = st.form_submit_button("Se connecter")

    if soumettre:
        try:
            with st.spinner("Connexion..."):
                reponse = api_client.connexion(identifiant, mot_de_passe)

        except api_client.ErreurApi as erreur:
            if erreur.status_code == 401:
                st.error("Identifiant ou mot de passe incorrect.")
            else:
                st.error(erreur.message)

        else:
            commun.connecter(identifiant, reponse)
            st.rerun()
else:
    st.success(f"Connecté en tant que {st.session_state['username']} (rôle : {st.session_state['role']})")
    st.write("Utilisez le menu latéral pour accéder aux écrans.")
    if st.button("Se déconnecter"):
        commun.deconnecter()
        st.rerun()