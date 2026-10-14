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
from decimal import Decimal, InvalidOperation



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
    """Vérifie qu'une station renseignée existe dans le référentiel
    une arrivée absente reste autorisée"""
    if station_id is None:
        raise ValueError("Référence de station absente")
    if station_id not in stations_connues:
        raise ValueError("Station inconnue")

def normaliser_texte_facultatif(valeur):
    """Renvoie None pour un champ absent, sinon le texte sans espaces autour
    pour les stations arrivées, pseudonyme, technicien, date résolution"""
    if valeur is None:
        return None
    texte = valeur.strip()
    if texte == "":
        return None
    return texte

def normaliser_texte_obligatoire(valeur, longueur_max):
    """Vérifie qu'un texte est présent et respecte la longueur maximale"""
    texte = normaliser_texte_facultatif(valeur)
    if texte is None:
        raise ValueError("Texte obligatoire absent")
    if len(texte) > longueur_max:
        raise ValueError("Texte trop long")
    return texte

def normaliser_station_id(station_id):
    """Normalise un identifiant de station et vérifie son format"""
    texte = normaliser_texte_obligatoire(station_id, 10)
    station_id_normalise = texte.upper()
    if re.fullmatch(r"S[0-9]{3}", station_id_normalise) is None:
        raise ValueError("Identifiant de station non reconnu")
    return station_id_normalise

def normaliser_trajet_id(trajet_id):
    """Normalise un identifiant de trajet et vérifie son format"""
    texte = normaliser_texte_obligatoire(trajet_id, 12)
    trajet_id_normalise = texte.upper()
    if re.fullmatch(r"T[0-9]{6}", trajet_id_normalise) is None:
        raise ValueError("Identifiant de trajet non reconnu")
    return trajet_id_normalise

def normaliser_incident_id(incident_id):
    """Normalise un identifiant d'incident et vérifie son format"""
    texte = normaliser_texte_obligatoire(incident_id, 12)
    incident_id_normalise = texte.upper()
    if re.fullmatch(r"I2026-[0-9]{4}", incident_id_normalise) is None:
        raise ValueError("Identifiant d'incident non reconnu")
    return incident_id_normalise

def normaliser_type_usager(type_usager):
    """Normalise le type d'usager et refuse les valeurs inconnues"""
    texte = normaliser_texte_obligatoire(type_usager, 20)
    type_normalise = texte.lower()
    if type_normalise not in ["abonne", "occasionnel"]:
        raise ValueError("Type d'usager non reconnu")
    return type_normalise

def normaliser_usager_ref(usager_ref):
    """Vérifie le format d'un pseudonyme lorsqu'il est renseigné"""
    texte = normaliser_texte_facultatif(usager_ref)
    if texte is None:
        return None
    if re.fullmatch(r"U[0-9A-Fa-f]{8}", texte) is None:
        raise ValueError("Pseudonyme d'usager non reconnu")
    return texte

def verifier_usager_ref(type_usager, usager_ref):
    """Vérifie la présence du pseudonyme selon le type d'usager"""
    if type_usager == "occasionnel":
        if usager_ref is not None:
            raise ValueError("Un usager occasionnel ne doit pas avoir de pseudonyme")
    elif type_usager == "abonne":
        if usager_ref is None:
            return "Pseudonyme absent pour un abonné"
    else:
        raise ValueError("Type d'usager non reconnu")
    return None

def verifier_technicien(statut, technicien):
    """Signale un technicien absent pour un incident pris en charge"""
    if statut in ["en_cours", "resolu"] and technicien is None:
        return "Technicien absent pour un incident pris en charge"
    return None

def verifier_type_incident(type_incident):
    """Vérifie que la catégorie d'incident est autorisée"""
    texte = normaliser_texte_obligatoire(type_incident, 100)
    types_autorises = [
        "vandalisme",
        "selle abimee",
        "eclairage HS",
        "chaine deraillee",
        "ecran borne illisible",
        "pneu creve",
        "frein defectueux",
        "borne hors service"]
    if texte not in types_autorises:
        raise ValueError("Type d'incident non reconnu")
    return texte

def convertir_coordonnee(valeur, minimum, maximum):
    """Convertit une coordonnée et vérifie ses limites"""
    texte = normaliser_texte_obligatoire(valeur, 100)
    try:
        coordonnee = Decimal(texte)
    except InvalidOperation:
        raise ValueError("Coordonnée non numérique")
    if coordonnee < minimum or coordonnee > maximum:
        raise ValueError("Coordonnée hors limites")
    return coordonnee

def normaliser_cible(cible):
    """Normalise la cible d'un incident et refuse les valeurs inconnues"""
    texte = normaliser_texte_obligatoire(cible, 20)
    cible_normalisee = texte.lower()
    if cible_normalisee not in ["velo", "station"]:
        raise ValueError("Cible non reconnue")
    return cible_normalisee