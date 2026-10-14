"""Routeur indicateurs.

À compléter : GET /indicateurs/activite-par-jour,
GET /indicateurs/stations-actives et
GET /indicateurs/incidents-par-statut.
"""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Utilisateur
from api.schemas import ActiviteParJourResponse, StationsActivesResponse, IncidentsParStatutResponse
from api.securite import utilisateur_courant
from api.services.indicateurs import activite_par_jour, stations_actives, incidents_par_statut

router = APIRouter(prefix="/indicateurs", tags=["Indicateurs"])

@router.get("/activite-par-jour", response_model=ActiviteParJourResponse)
def consulter_activite_par_jour(
    date_debut: date | None = None,
    date_fin: date | None = None,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(utilisateur_courant)):
    return activite_par_jour(db, date_debut, date_fin)

@router.get("/stations-actives", response_model=StationsActivesResponse)
def consulter_stations_actives(
    limite: int = Query(default=10, ge=1),
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(utilisateur_courant)):
    return stations_actives(db, limite)

@router.get("/incidents-par-statut", response_model=IncidentsParStatutResponse)
def consulter_incidents_par_statut(
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(utilisateur_courant)):
    return incidents_par_statut(db)