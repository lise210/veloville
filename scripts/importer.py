"""Import et fiabilisation des trois exports CSV dans PostgreSQL.

À compléter : lire data/stations.csv, data/trajets.csv et data/incidents.csv,
appliquer les règles de fiabilisation (api/services/fiabilisation.py),
charger les lignes valides, journaliser les rejets et les avertissements.
Le script doit être idempotent : deux exécutions successives laissent la
base dans le même état.

Usage prévu : python scripts/importer.py [--dossier data]
Usage actuel : python -m scripts.importer
"""

import pandas as pd 

from api.services.fiabilisation import separer_doublons

def main() -> None:
    #keep_default_na=False : garde les champs vides comme ""
    #dtype=str : lit toutes les valeurs comme du texte (utilisation de .strip() dans mes fonctions dvpéesqui focntionne pour du texte)
    stations = pd.read_csv("data/stations.csv", dtype=str, keep_default_na=False)
    trajets = pd.read_csv("data/trajets.csv", dtype=str, keep_default_na=False)
    incidents = pd.read_csv("data/incidents.csv", dtype=str, keep_default_na=False)

    print("Stations lues :", len(stations))
    print("Trajets lus :", len(trajets))
    print("Incidents lus :", len(incidents))

    #prepare ligne pour fonction separer_doublons
    #to_dict(orient="records") : convertir un DataFrame Pandas en une liste de dictionnaires Python, où chaque ligne devient un dictionnaire.
    lignes_trajets = trajets.to_dict(orient="records")
    trajets_uniques, trajets_doublons = separer_doublons(lignes_trajets)
    print("Doublons de trajets écartés :", len(trajets_doublons))
    print("Trajets sans doublons :", len(trajets_uniques))   


if __name__ == "__main__":
    main()
