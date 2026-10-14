"""Calcul des trois indicateurs (module métier testé).

À compléter : activite_par_jour(session, date_debut, date_fin),
stations_actives(session, limite) et incidents_par_statut(session).
Les routeurs ne font qu'appeler ces fonctions.
"""
from sqlalchemy import select, func
from sqlalchemy.orm import aliased

from api.models import Trajet, Station, Incident

def activite_par_jour(session, date_debut=None, date_fin=None):
    """Indicateur « activité par jour » : nombre de trajets par jour sur une période"""
    #func.date() récupère le jour sans l’heure
    jour = func.date(Trajet.depart_horodatage)
    #func.count() compte les trajets
    #label() nomme les colonnes du résultat
    requete = select(jour.label("jour"), func.count(Trajet.trajet_id).label("nb_trajets"))
    if date_debut is not None:
        requete = requete.where(jour >= date_debut)
    if date_fin is not None:
        requete = requete.where(jour <= date_fin)
    requete = requete.group_by(jour).order_by(jour)
    resultats = session.execute(requete).all()
    donnees = []
    for resultat in resultats:
        #isoformat() date comme "2026-08-24"
        donnees.append({"jour": resultat.jour.isoformat(), "nb_trajets": resultat.nb_trajets})
    return {"donnees": donnees}

def stations_actives(session, limite=10):
    """Indicateur « stations actives » : les stations ayant le plus de départs et d'arrivées"""
    #aliased permet d'utiliser deux fois la table trajet
    depart = aliased(Trajet)
    arrivee = aliased(Trajet)
    nb_departs = func.count(depart.trajet_id.distinct())
    nb_arrivees = func.count(arrivee.trajet_id.distinct())
    requete = (
        select(
            Station.station_id,
            Station.nom,
            nb_departs.label("nb_departs"),
            nb_arrivees.label("nb_arrivees"))
        .select_from(Station)
        #outerjoin() : équivalent de LEFT JOIN en SQL
        .outerjoin(depart, depart.station_depart == Station.station_id)
        .outerjoin(arrivee, arrivee.station_arrivee == Station.station_id)
        .group_by(Station.station_id, Station.nom)
        .order_by((nb_departs + nb_arrivees).desc(), Station.station_id.asc())
        .limit(limite))

    resultats = session.execute(requete).all()
    donnees = []
    for resultat in resultats:
        donnees.append({
            "station_id": resultat.station_id,
            "nom": resultat.nom,
            "nb_departs": resultat.nb_departs,
            "nb_arrivees": resultat.nb_arrivees})
    return {"donnees": donnees}



def incidents_par_statut(session):
    """Indicateur « incidents par statut » : répartition des incidents et délai moyen de résolution"""
    requete_statuts = (select(Incident.statut, func.count(Incident.incident_id).label("nb_incidents"))
        .group_by(Incident.statut)
        .order_by(Incident.statut))

    resultats = session.execute(requete_statuts).all()
    donnees = []
    for resultat in resultats:
        donnees.append({
            "statut": resultat.statut,
            "nb_incidents": resultat.nb_incidents})

    duree_heures = func.extract(
        "epoch",  #dit uqe je veux la durée en seconde
        Incident.date_resolution - Incident.date_signalement,
    ) / 3600

    requete_delai = (
        select(func.round(func.avg(duree_heures), 1))
        .where(Incident.statut == "resolu")
        .where(Incident.date_resolution.is_not(None)))

    delai = session.scalar(requete_delai)

    if delai is not None:
        delai = float(delai)

    return {
        "donnees": donnees,
        "delai_moyen_resolution_heures": delai}