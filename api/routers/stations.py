"""Routeur stations.

À compléter : GET /stations (filtre commune, pagination) et GET /stations/{station_id}.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Station, Utilisateur
from api.schemas import StationResponse, StationsPagineesResponse
from api.securite import utilisateur_courant
from api.services.stations import lister_stations

router = APIRouter(prefix="/stations", tags=["Stations"])

@router.get("", response_model=StationsPagineesResponse)
def consulter_stations(
    commune: str | None = None,
    page: int = Query(default=1, ge=1),  #default=1 : sans précision, on utilise la page 1. ge=1 : la valeur doit être supérieure ou égale à 1.
    taille_page: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(utilisateur_courant)):
    """Renvoie les stations filtrées et paginées"""
    return lister_stations(
        db,
        commune=commune,
        page=page,
        taille_page=taille_page)

@router.get("/{station_id}", response_model=StationResponse)
def consulter_station(
    station_id: str,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(utilisateur_courant)):
    """Renvoie une station pour un utilisateur authentifié"""
    station = db.scalar(select(Station).where(Station.station_id == station_id))

    if station is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station introuvable")
    return station