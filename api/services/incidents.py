"""Consultation des incidents."""

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

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


def changer_statut_incident(
    db: Session,
    incident_id: str,
    nouveau_statut: str):
    """Vérifie la transition puis enregistre le nouveau statut"""
    incident = db.scalar(select(Incident).where(Incident.incident_id == incident_id))
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident introuvable")
    transition_autorisee = (incident.statut == "ouvert" and nouveau_statut in ("en_cours", "resolu")
                              ) or (incident.statut == "en_cours" and nouveau_statut == "resolu")
    if not transition_autorisee:
        raise HTTPException(status_code=422, detail="Transition de statut non autorisee")
    incident.statut = nouveau_statut
    if nouveau_statut == "resolu" and incident.date_resolution is None:
        incident.date_resolution = datetime.now()

    db.commit()
    db.refresh(incident)
    return incident

