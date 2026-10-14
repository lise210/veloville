"""Routeur incidents.

À compléter : GET /incidents (filtre statut, pagination) et
PUT /incidents/{incident_id}/statut (rôle exploitant).
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Utilisateur
from api.schemas import IncidentsPaginesResponse, IncidentResponse, ChangementStatutRequest
from api.securite import utilisateur_courant, exiger_role
from api.services.incidents import lister_incidents, changer_statut_incident

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


@router.put("/{incident_id}/statut", response_model=IncidentResponse)
def modifier_statut_incident(
    incident_id: str,
    data: ChangementStatutRequest,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(exiger_role("exploitant"))):
    """Modifie le statut d'un incident pour le rôle exploitant"""
    return changer_statut_incident(db, incident_id=incident_id, nouveau_statut=data.statut)