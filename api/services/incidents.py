"""Consultation des incidents."""

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from api.models import Incident

def lister_incidents(
    db: Session,
    statut: str | None = None,
    page: int = 1,
    taille_page: int = 20):
    """Recherche les incidents et sélectionne une page"""
    requete = select(Incident)
    comptage = select(func.count()).select_from(Incident)

    if statut is not None:
        requete = requete.where(Incident.statut == statut)
        comptage = comptage.where(Incident.statut == statut)

    total = db.scalar(comptage)
    decalage = (page - 1) * taille_page
    incidents = db.scalars(
        requete
        .order_by(Incident.date_signalement.desc(), Incident.incident_id)
        .offset(decalage)
        .limit(taille_page)
    ).all()

    return {
        "total": total,
        "page": page,
        "taille_page": taille_page,
        "resultats": incidents}