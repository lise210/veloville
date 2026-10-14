"""Schémas Pydantic (entrées et sorties de l'API).

À compléter : schémas de lecture des trois ressources, enveloppe paginée, corps de
connexion, réponse de connexion, corps de changement de statut, réponses
des trois indicateurs.
"""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

class LoginRequest(BaseModel):
    """Identifiants envoyés pour se connecter"""
    username: str
    password: str

class TokenResponse(BaseModel):
    """Réponse après une connexion réussie"""
    access_token: str
    token_type: str = "bearer"
    role: str


class StationResponse(BaseModel):
    """Données d'une station renvoyées par l'API"""
    model_config = ConfigDict(from_attributes=True)
    station_id: str
    nom: str
    commune: str
    capacite: int
    latitude: Decimal
    longitude: Decimal
    date_mise_en_service: date


class StationsPagineesResponse(BaseModel):
    """Une page de stations et ses informations de pagination"""
    total: int
    page: int
    taille_page: int
    resultats: list[StationResponse]


class TrajetResponse(BaseModel):
    """Données d'un trajet renvoyées par l'API"""
    model_config = ConfigDict(from_attributes=True)
    trajet_id: str
    velo_id: str
    depart_horodatage: datetime
    station_depart: str
    station_arrivee: str | None
    duree_secondes: int
    type_usager: str
    usager_ref: str | None


class TrajetsPaginesResponse(BaseModel):
    """Une page de trajets et ses informations de pagination"""
    total: int
    page: int
    taille_page: int
    resultats: list[TrajetResponse]


class IncidentResponse(BaseModel):
    """Données d'un incident renvoyées par l'API"""
    model_config = ConfigDict(from_attributes=True)
    incident_id: str
    date_signalement: datetime
    cible: str
    velo_id: str | None
    station_id: str | None
    type_incident: str
    statut: str
    date_resolution: datetime | None
    technicien: str | None


class IncidentsPaginesResponse(BaseModel):
    """Une page d'incidents et ses informations de pagination"""
    total: int
    page: int
    taille_page: int
    resultats: list[IncidentResponse]


class ChangementStatutRequest(BaseModel):
    """Nouveau statut demandé pour un incident"""
    statut: str