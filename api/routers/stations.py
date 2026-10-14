"""Routeur stations.

À compléter : GET /stations (filtre commune, pagination) et GET /stations/{station_id}.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Station, Utilisateur
from api.schemas import StationResponse
from api.securite import utilisateur_courant

router = APIRouter(prefix="/stations", tags=["Stations"])

@router.get("/{station_id}", response_model=StationResponse)
def consulter_station(
    station_id: str,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(utilisateur_courant)):
    """Renvoie une station pour un utilisateur authentifié"""
    station = db.scalar(select(Station).where(Station.station_id == station_id))

    if station is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Station inconnue")
    return station