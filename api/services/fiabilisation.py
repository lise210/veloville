"""Règles de fiabilisation des données (module métier testé).

À compléter : fonctions pures, sans accès à la base, qui normalisent ou rejettent
une valeur ou une ligne : horodatages, identifiants de vélo, statuts
d'incident, durées, références de station, cohérence des dates,
doublons. Chaque fonction retourne la valeur normalisée ou signale le
motif de rejet. Ces fonctions sont appelées par scripts/importer.py et
couvertes par tests/unit/.
"""

def normaliser_statut(statut):
    """Normalise un statut et refuse les valeurs inconnues"""
    if statut is None:
        raise ValueError("Statut absent")
    statut_normalise = statut.strip().lower().replace(" ", "_")
    if statut_normalise not in ["ouvert", "en_cours", "resolu"]:
        raise ValueError("Statut non reconnu")
    return statut_normalise

