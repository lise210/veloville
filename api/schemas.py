"""Schémas Pydantic (entrées et sorties de l'API).

À compléter : schémas de lecture des trois ressources, enveloppe paginée, corps de
connexion, réponse de connexion, corps de changement de statut, réponses
des trois indicateurs.
"""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Identifiants envoyés pour se connecter"""
    username: str
    password: str

class TokenResponse(BaseModel):
    """Réponse après une connexion réussie"""
    access_token: str
    token_type: str = "bearer"
    role: str