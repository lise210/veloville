"""Client HTTP centralisé vers l'API VéloVille.

À compléter : lire API_URL et API_TIMEOUT_SECONDES, ajouter l'en-tête
Authorization: Bearer <jeton>, lever ErreurApi (message en français)
sur erreur réseau, délai dépassé ou code HTTP d'erreur.
"""

import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class ErreurApi(Exception):
    """Erreur levée lorsque l'API est injoignable ou répond en erreur."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

def _api_url() -> str:
    """Retourne l'adresse de l'API."""
    return os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")

def _timeout() -> float:
    """Retourne le délai maximal d'un appel HTTP."""
    return float(os.getenv("API_TIMEOUT_SECONDES", "5"))

def _headers() -> dict[str, str]:
    """Ajoute le JWT enregistré dans la session Streamlit."""
    token = st.session_state.get("access_token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}

def appeler(
    method: str,
    path: str,
    *,
    params: dict | None = None,
    json: dict | None = None,
) -> dict:
    """Effectue un appel HTTP vers l'API"""
    try:
        reponse = requests.request(
            method=method,
            url=f"{_api_url()}{path}",
            params=params,
            json=json,
            headers=_headers(),
            timeout=_timeout())
    except requests.exceptions.Timeout as erreur:
        raise ErreurApi("L'API n'a pas répondu dans le délai prévu") from erreur
    except requests.exceptions.RequestException as erreur:
        raise ErreurApi("Impossible de joindre l'API") from erreur
    if reponse.ok:
        return reponse.json()
    messages = {
        401: "Session absente, invalide ou expirée",
        403: "Votre rôle ne permet pas cet accès",
        404: "Ressource introuvable",
        422: "Paramètres invalides"}

    raise ErreurApi(messages.get(reponse.status_code, f"Erreur API ({reponse.status_code})."), status_code=reponse.status_code)


def connexion(username: str, password: str) -> dict:
    """Appelle la route de connexion."""
    return appeler("POST", "/auth/login",
        json={
            "username": username,
            "password": password})

def obtenir(path: str, params: dict | None = None) -> dict:
    """Récupère des données depuis l'API."""
    return appeler("GET",
        path,
        params=params)


def modifier_statut(incident_id: str, statut: str) -> dict:
    """Demande le changement de statut d'un incident"""
    return appeler("PUT", f"/incidents/{incident_id}/statut", json={"statut": statut})