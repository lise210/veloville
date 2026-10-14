"""Routeur trajets.

À compléter : GET /trajets (filtres date_debut, date_fin, station ; pagination).
"""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Utilisateur
from api.schemas import TrajetsPaginesResponse
from api.securite import utilisateur_courant
from api.services.trajets import lister_trajets

router = APIRouter(prefix="/trajets", tags=["Trajets"])

@router.get("", response_model=TrajetsPaginesResponse)
def consulter_trajets(
    date_debut: date | None = None,
    date_fin: date | None = None,
    station: str | None = None,
    page: int = Query(default=1, ge=1),
    taille_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(utilisateur_courant)):
    """Renvoie les trajets filtrés et paginés"""
    return lister_trajets(
        db,
        date_debut=date_debut,
        date_fin=date_fin,
        station=station,
        page=page,
        taille_page=taille_page)