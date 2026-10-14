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
        date_convertie = datetime.strptime(texte, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date impossible") from None
    return date_convertie.date()