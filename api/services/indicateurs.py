"""Calcul des trois indicateurs (module métier testé).

À compléter : activite_par_jour(session, date_debut, date_fin),
stations_actives(session, limite) et incidents_par_statut(session).
Les routeurs ne font qu'appeler ces fonctions.
"""
from sqlalchemy import select, func
from api.models import Trajet

def activite_par_jour(session, date_debut=None, date_fin=None):
    """Compte les trajets par jour, sur une période facultative"""
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