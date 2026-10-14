"""Routeur incidents.

À compléter : GET /incidents (filtre statut, pagination) et
PUT /incidents/{incident_id}/statut (rôle exploitant).
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Utilisateur
from api.schemas import IncidentsPaginesResponse
from api.securite import utilisateur_courant
from api.services.incidents import lister_incidents

router = APIRouter(prefix="/incidents", tags=["Incidents"])

@router.get("", response_model=IncidentsPaginesResponse)
def consulter_incidents(
    statut: str | None = None,
    page: int = Query(default=1, ge=1),
    taille_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(utilisateur_courant)):
    """Renvoie les incidents filtrés et paginés"""
    return lister_incidents(
        db,
        statut=statut,
        page=page,
        taille_page=taille_page)