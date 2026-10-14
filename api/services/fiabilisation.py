"""Règles de fiabilisation des données (module métier testé).

À compléter : fonctions pures, sans accès à la base, qui normalisent ou rejettent
une valeur ou une ligne : horodatages, identifiants de vélo, statuts
d'incident, durées, références de station, cohérence des dates,
doublons. Chaque fonction retourne la valeur normalisée ou signale le
motif de rejet. Ces fonctions sont appelées par scripts/importer.py et
couvertes par tests/unit/.
"""

import re
from datetime import datetime



def normaliser_statut(statut):
    """Normalise un statut et refuse les valeurs inconnues"""
    if statut is None:
        raise ValueError("Statut absent")
    statut_normalise = statut.strip().lower().replace(" ", "_")
    if statut_normalise not in ["ouvert", "en_cours", "resolu"]:
        raise ValueError("Statut non reconnu")
    return statut_normalise

def normaliser_velo_id(velo_id):
    """Met l'identifiant du vélo en majuscules et vérifie son format"""
    if velo_id is None:
        raise ValueError("Identifiant de vélo absent")
    velo_id_normalise = velo_id.strip().upper()
    #re.fullmatch() : vérifie toute la valeur : V + chiffres
    if re.fullmatch(r"V[0-9]{4}", velo_id_normalise) is None:
        raise ValueError("Identifiant de vélo non reconnu")
    return velo_id_normalise

def convertir_entier_positif(valeur):
    """Convertit une valeur du CSV en entier strictement positif"""
    if valeur is None:
        raise ValueError("Valeur absente")
    texte = str(valeur).strip()
    if re.fullmatch(r"[+-]?[0-9]+", texte) is None:
        raise ValueError("Valeur non entière")
    entier = int(texte)
    if entier <= 0:
        raise ValueError("Valeur non positive")
    return entier

def convertir_date(valeur):
    """Convertit une date au format AAAA-MM-JJ"""
    if valeur is None:
        raise ValueError("Date absente")
    texte = valeur.strip()
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", texte) is None:
        raise ValueError("Format de date non reconnu")
    try:
        #datetime.strptime() : permet de convertir une chaîne de caractères représentant une date et une heure en un objet datetime, selon un format spécifié
        date_convertie = datetime.strptime(texte, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date impossible") from None
    return date_convertie.date()

def convertir_horodatage(valeur):
    """Convertit une date et une heure dans les formats acceptés"""
    if valeur is None:
        raise ValueError("Horodatage absent")
    texte = valeur.strip()
    formats_acceptes = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M"]
    for format_date in formats_acceptes:
        try:
            return datetime.strptime(texte, format_date)
        except ValueError:
            #si échoue, passe au format suivant
            continue
    raise ValueError("Horodatage impossible ou format non reconnu")

def verifier_dates_incident(statut, date_signalement, date_resolution):
    """Vérifie les dates d'un incident selon son statut."""
    if statut == "resolu":
        if date_resolution is None:
            raise ValueError("Incident résolu sans date de résolution")
        if date_resolution < date_signalement:
            raise ValueError("Résolution antérieure au signalement")
    elif date_resolution is not None:
        raise ValueError("Incident non résolu avec une date de résolution")

def verifier_cible_incident(cible, velo_id, station_id):
    """Vérifie que les références correspondent à la cible"""
    if cible == "velo":
        if velo_id is None or station_id is not None:
            raise ValueError("Références incorrectes pour un incident vélo")
    elif cible == "station":
        if station_id is None or velo_id is not None:
            raise ValueError("Références incorrectes pour un incident station")
    else:
        raise ValueError("Cible non reconnue")

def verifier_reference_station(station_id, stations_connues):
    """Vérifie qu'une station renseignée existe dans le référentiel"""
    if station_id is None:
        raise ValueError("Référence de station absente")
    if station_id not in stations_connues:
        raise ValueError("Station inconnue")