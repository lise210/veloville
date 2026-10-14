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
from decimal import InvalidOperation

from api.services.fiabilisation import separer_doublons, normaliser_station_id, normaliser_texte_obligatoire, convertir_coordonnee, convertir_date, convertir_entier_positif, normaliser_trajet_id, normaliser_velo_id, convertir_horodatage, verifier_reference_station, normaliser_texte_facultatif, normaliser_type_usager, normaliser_usager_ref, verifier_usager_ref

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

    lignes_stations = stations.to_dict(orient="records")
    stations_valides = []
    journal = []

    # journalise chaque répétition de trajet écartée
    for ligne in trajets_doublons:
        journal.append({
            "fichier_source": "trajets.csv",
            "identifiant": ligne["trajet_id"],
            "colonne": "trajet_id",
            "valeur": ligne["trajet_id"],
            "motif": "Ligne strictement identique déjà traitée",
            "decision": "doublon"})

    #boucle station
    for ligne in lignes_stations:
        try:
            colonne = "station_id"
            station_id = normaliser_station_id(ligne[colonne])
            colonne = "nom"
            nom = normaliser_texte_obligatoire(ligne[colonne], 100)
            colonne = "commune"
            commune = normaliser_texte_obligatoire(ligne[colonne], 100)
            colonne = "capacite"
            capacite = convertir_entier_positif(ligne[colonne])
            colonne = "latitude"
            latitude = convertir_coordonnee(ligne[colonne], -90, 90)
            colonne = "longitude"
            longitude = convertir_coordonnee(ligne[colonne], -180, 180)
            colonne = "date_mise_en_service"
            date_mise_en_service = convertir_date(ligne[colonne])
            stations_valides.append({
                "station_id": station_id,
                "nom": nom,
                "commune": commune,
                "capacite": capacite,
                "latitude": latitude,
                "longitude": longitude,
                "date_mise_en_service": date_mise_en_service,
            })

        except (ValueError, InvalidOperation) as erreur:
            print(f"Station refusée : {ligne["station_id"]} - {erreur}")
            journal.append({
                "fichier_source": "stations.csv",
                "identifiant": ligne["station_id"],
                "colonne": colonne,
                "valeur": ligne[colonne],
                "motif": str(erreur),
                "decision": "rejet",
            })

            print(f"Station refusée : {ligne['station_id']} - {erreur}")

    print("Stations valides :", len(stations_valides))
    # id des stations ayant passé tous les contrôles
    stations_connues = []
    for station in stations_valides:
        stations_connues.append(station["station_id"])
    print("Stations dans le référentiel :", len(stations_connues))

    # Contrôle des trajets sans doublons.
    trajets_valides = []
    for ligne in trajets_uniques:
        try:
            colonne = "trajet_id"
            trajet_id = normaliser_trajet_id(ligne[colonne])
            colonne = "velo_id"
            velo_id = normaliser_velo_id(ligne[colonne])
            colonne = "depart_horodatage"
            depart_horodatage = convertir_horodatage(ligne[colonne])
            colonne = "station_depart"
            station_depart = normaliser_station_id(ligne[colonne])
            verifier_reference_station(station_depart, stations_connues)  
            colonne = "station_arrivee"
            station_arrivee = normaliser_texte_facultatif(ligne[colonne])
            if station_arrivee is not None:
                station_arrivee = normaliser_station_id(station_arrivee)
                verifier_reference_station(station_arrivee, stations_connues)  
            colonne = "duree_secondes"
            duree_secondes = convertir_entier_positif(ligne[colonne])
            colonne = "type_usager"
            type_usager = normaliser_type_usager(ligne[colonne])
            colonne = "usager_ref"
            usager_ref = normaliser_usager_ref(ligne[colonne])
            avertissement = verifier_usager_ref(type_usager, usager_ref)
            if avertissement is not None:
                journal.append({
                    "fichier_source": "trajets.csv",
                    "identifiant": ligne["trajet_id"],
                    "colonne": colonne,
                    "valeur": ligne[colonne],
                    "motif": avertissement,
                    "decision": "avertissement"})
            trajets_valides.append({
                "trajet_id": trajet_id,
                "velo_id": velo_id,
                "depart_horodatage": depart_horodatage,
                "station_depart": station_depart,
                "station_arrivee": station_arrivee,
                "duree_secondes": duree_secondes,
                "type_usager": type_usager,
                "usager_ref": usager_ref})
        except ValueError as erreur:
            journal.append({
                "fichier_source": "trajets.csv",
                "identifiant": ligne["trajet_id"],
                "colonne": colonne,
                "valeur": ligne[colonne],
                "motif": str(erreur),
                "decision": "rejet"})
            print(f"Trajet refusé : {ligne['trajet_id']} - {erreur}")
   
    print("Trajets valides :", len(trajets_valides))
   
    print("Messages dans le journal :", len(journal))

    colonnes_journal = [
        "fichier_source",
        "identifiant",
        "colonne",
        "valeur",
        "motif",
        "decision"]

    pd.DataFrame(journal, columns=colonnes_journal).to_csv("docs/journal_import.csv", index=False, encoding="utf-8")


if __name__ == "__main__":
    main()
