"""Consultation des trajets"""

from datetime import date

from sqlalchemy import select, func, or_ #or_ equivaut à OU en SQL
from sqlalchemy.orm import Session

from api.models import Trajet

def lister_trajets(
    db: Session,
    date_debut: date | None = None,
    date_fin: date | None = None,
    station: str | None = None,
    page: int = 1,
    taille_page: int = 20):
    """Recherche les trajets et sélectionne une page"""
    requete = select(Trajet)
    comptage = select(func.count()).select_from(Trajet)

    if date_debut is not None:
        condition = func.date(Trajet.depart_horodatage) >= date_debut
        requete = requete.where(condition)
        comptage = comptage.where(condition)

    if date_fin is not None:
        condition = func.date(Trajet.depart_horodatage) <= date_fin
        requete = requete.where(condition)
        comptage = comptage.where(condition)

    if station is not None:
        condition = or_(Trajet.station_depart == station, Trajet.station_arrivee == station)
        requete = requete.where(condition)
        comptage = comptage.where(condition)

    total = db.scalar(comptage)
    decalage = (page - 1) * taille_page

    trajets = db.scalars(
        requete
        .order_by(Trajet.depart_horodatage, Trajet.trajet_id)
        .offset(decalage)
        .limit(taille_page)
    ).all()

    return {
        "total": total,
        "page": page,
        "taille_page": taille_page,
        "resultats": trajets}