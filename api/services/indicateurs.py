"""Calcul des trois indicateurs (module métier testé).

À compléter : activite_par_jour(session, date_debut, date_fin),
stations_actives(session, limite) et incidents_par_statut(session).
Les routeurs ne font qu'appeler ces fonctions.
"""
from sqlalchemy import select, func
from sqlalchemy.orm import aliased

from api.models import Trajet, Station

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


"""Indicateur « incidents par statut » : répartition des incidents et délai moyen de résolution"""