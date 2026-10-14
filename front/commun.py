"""Gestion de la session Streamlit"""

import streamlit as st

def est_connecte() -> bool:
    """Indique si un jeton est présent dans la session"""
    return bool(st.session_state.get("access_token"))

def connecter(username: str, reponse: dict) -> None:
    """Mémorise le jeton, l'identifiant et le rôle"""
    st.session_state["access_token"] = reponse["access_token"]
    st.session_state["username"] = username
    st.session_state["role"] = reponse["role"]

def deconnecter() -> None:
    """Efface les informations de connexion"""
    for info in ("access_token", "username", "role"):
        st.session_state.pop(info, None)