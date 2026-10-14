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

from api.services.fiabilisation import separer_doublons, normaliser_station_id, normaliser_texte_obligatoire, convertir_coordonnee, convertir_date, convertir_entier_positif, normaliser_trajet_id, normaliser_velo_id, convertir_horodatage, verifier_reference_station, normaliser_texte_facultatif, normaliser_type_usager, normaliser_usager_ref, verifier_usager_ref, normaliser_incident_id, normaliser_statut, normaliser_cible, verifier_cible_incident, verifier_type_incident, verifier_dates_incident, verifier_technicien

from sqlalchemy import select
from api.database import SessionLocal
from api.models import Station, Trajet, Incident

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

            if velo_id != ligne[colonne]:
                journal.append({
                    "fichier_source": "trajets.csv",
                    "identifiant": ligne["trajet_id"],
                    "colonne": colonne,
                    "valeur": ligne[colonne],
                    "motif": f"Identifiant de vélo normalisé en {velo_id}",
                    "decision": "normalisation"})

            colonne = "depart_horodatage"
            depart_horodatage = convertir_horodatage(ligne[colonne])

            horodatage_normalise = depart_horodatage.strftime("%Y-%m-%d %H:%M:%S")
            if horodatage_normalise != ligne[colonne]:
                journal.append({
                    "fichier_source": "trajets.csv",
                    "identifiant": ligne["trajet_id"],
                    "colonne": colonne,
                    "valeur": ligne[colonne],
                    "motif": f"Horodatage normalisé en {horodatage_normalise}",
                    "decision": "normalisation"})

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

    # Contrôle des incidents
    lignes_incidents = incidents.to_dict(orient="records")
    incidents_valides = []
    for ligne in lignes_incidents:
        try:
            colonne = "incident_id"
            incident_id = normaliser_incident_id(ligne[colonne])
            colonne = "statut"
            statut = normaliser_statut(ligne[colonne])
            if statut != ligne[colonne]:
                journal.append({
                    "fichier_source": "incidents.csv",
                    "identifiant": ligne["incident_id"],
                    "colonne": colonne,
                    "valeur": ligne[colonne],
                    "motif": f"Statut normalisé en {statut}",
                    "decision": "normalisation"})
            colonne = "date_signalement"
            date_signalement = convertir_horodatage(ligne[colonne])
            colonne = "cible"
            cible = normaliser_cible(ligne[colonne])
            colonne = "velo_id"
            velo_id_incident = normaliser_texte_facultatif(ligne[colonne])
            if velo_id_incident is not None:
                velo_id_incident = normaliser_velo_id(velo_id_incident)
            colonne = "station_id"
            station_id_incident = normaliser_texte_facultatif(ligne[colonne])
            if station_id_incident is not None:
                station_id_incident = normaliser_station_id(station_id_incident)
                verifier_reference_station(station_id_incident, stations_connues)
            colonne = "cible"
            verifier_cible_incident(cible, velo_id_incident, station_id_incident)
            colonne = "type_incident"
            type_incident = verifier_type_incident(ligne[colonne])
            colonne = "date_resolution"
            date_resolution = normaliser_texte_facultatif(ligne[colonne])
            if date_resolution is not None:
                date_resolution = convertir_horodatage(date_resolution)
            verifier_dates_incident(statut, date_signalement, date_resolution)
            colonne = "technicien"
            technicien = normaliser_texte_facultatif(ligne[colonne])
            if technicien is not None:
                technicien = normaliser_texte_obligatoire(technicien, 100)
            avertissement = verifier_technicien(statut, technicien)
            if avertissement is not None:
                journal.append({
                    "fichier_source": "incidents.csv",
                    "identifiant": ligne["incident_id"],
                    "colonne": colonne,
                    "valeur": ligne[colonne],
                    "motif": avertissement,
                    "decision": "avertissement"})
            incidents_valides.append({
                "incident_id": incident_id,
                "date_signalement": date_signalement,
                "cible": cible,
                "velo_id": velo_id_incident,
                "station_id": station_id_incident,
                "type_incident": type_incident,
                "statut": statut,
                "date_resolution": date_resolution,
                "technicien": technicien})
        except ValueError as erreur:
            journal.append({
                "fichier_source": "incidents.csv",
                "identifiant": ligne["incident_id"],
                "colonne": colonne,
                "valeur": ligne[colonne],
                "motif": str(erreur),
                "decision": "rejet"})
            print(f"Incident refusé : {ligne['incident_id']} - {erreur}")

    print("Incidents valides :", len(incidents_valides))

    print("Messages dans le journal :", len(journal))

    colonnes_journal = [
        "fichier_source",
        "identifiant",
        "colonne",
        "valeur",
        "motif",
        "decision"]

    pd.DataFrame(journal, columns=colonnes_journal).to_csv("docs/journal_import.csv", index=False, encoding="utf-8")

    #charge dans la bdd les stations uniquement si leur identifiant est absent
    with SessionLocal() as db:
        for station in stations_valides:
            station_existante = db.scalar(select(Station).where(Station.station_id == station["station_id"]))
            if station_existante is None:
                nouvelle_station = Station(
                    station_id=station["station_id"],
                    nom=station["nom"],
                    commune=station["commune"],
                    capacite=station["capacite"],
                    latitude=station["latitude"],
                    longitude=station["longitude"],
                    date_mise_en_service=station["date_mise_en_service"])
                db.add(nouvelle_station)
        
        # Envoie les nouvelles stations à PostgreSQL sans valider la transaction.
        db.flush()
        for trajet in trajets_valides:
            trajet_existant = db.scalar(select(Trajet).where(Trajet.trajet_id == trajet["trajet_id"]))
            if trajet_existant is None:
                nouveau_trajet = Trajet(
                    trajet_id=trajet["trajet_id"],
                    velo_id=trajet["velo_id"],
                    depart_horodatage=trajet["depart_horodatage"],
                    station_depart=trajet["station_depart"],
                    station_arrivee=trajet["station_arrivee"],
                    duree_secondes=trajet["duree_secondes"],
                    type_usager=trajet["type_usager"],
                    usager_ref=trajet["usager_ref"])
                db.add(nouveau_trajet)

        for incident in incidents_valides:
            incident_existant = db.scalar(select(Incident).where(Incident.incident_id == incident["incident_id"]))
            if incident_existant is None:
                nouvel_incident = Incident(
                    incident_id=incident["incident_id"],
                    date_signalement=incident["date_signalement"],
                    cible=incident["cible"],
                    velo_id=incident["velo_id"],
                    station_id=incident["station_id"],
                    type_incident=incident["type_incident"],
                    statut=incident["statut"],
                    date_resolution=incident["date_resolution"],
                    technicien=incident["technicien"])
                db.add(nouvel_incident)

        db.commit()
    print("Chargement des stations, trajets et incidents terminé.")
    
if __name__ == "__main__":
    main()
