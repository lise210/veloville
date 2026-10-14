"""Règles de fiabilisation des données (module métier testé).

À compléter : fonctions pures, sans accès à la base, qui normalisent ou rejettent
une valeur ou une ligne : horodatages, identifiants de vélo, statuts
d'incident, durées, références de station, cohérence des dates,
doublons. Chaque fonction retourne la valeur normalisée ou signale le
motif de rejet. Ces fonctions sont appelées par scripts/importer.py et
couvertes par tests/unit/.
"""

import re

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