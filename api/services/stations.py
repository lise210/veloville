"""Consultation des stations"""

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from api.models import Station

def lister_stations(
    db: Session,
    commune: str | None = None,
    page: int = 1,
    taille_page: int = 20):
    """Recherche les stations et sélectionne une page"""
    requete = select(Station)
    comptage = select(func.count()).select_from(Station)

    if commune is not None:
        requete = requete.where(Station.commune == commune)
        comptage = comptage.where(Station.commune == commune)

    total = db.scalar(comptage)
    decalage = (page - 1) * taille_page
    stations = db.scalars(
        requete
        .order_by(Station.station_id)
        .offset(decalage)
        .limit(taille_page)
    ).all()

    return {
        "total": total,
        "page": page,
        "taille_page": taille_page,
        "resultats": stations}