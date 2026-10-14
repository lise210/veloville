"""Audit des exports CSV avant leur import dans PostgreSQL"""
###########################################################################Stations###########################
import pandas as pd

print("\n--- AUDIT DES STATIONS ---")

stations = pd.read_csv("data/stations.csv")

# affiche les 5 premières lignes
print(stations.head())

#nb lignes et colonnes
print("Nombre de lignes :", stations.shape[0])
print("Nombre de colonnes :", stations.shape[1])

#nb valeurs manquantes dans chaque colonne
print(f"\nValeurs manquantes : {stations.isna().sum()}")

# Doublons 
print(f"\nNombre de lignes dupliquées : {stations.duplicated().sum()}")
print(f"Nombre d'identifiants répétés : {stations['station_id'].duplicated().sum()}")

# RG1 : capacité strictement positive
capacites_invalides = stations[stations["capacite"] <= 0]
print(f"\nNombre de capacités invalides : {len(capacites_invalides)}")

# identifiant attendu : S + 3 chiffres
#fullmatch() : vérif que j'ai bien S + 3 chiffres
# ~ inverse (ici donne sum(identifiants_valides))
identifiants_valides = stations["station_id"].str.fullmatch(r"S[0-9]{3}", na=False)
print(f"\nNombre d'identifiants au mauvais format : {(~identifiants_valides).sum()}")

# Vérif dates peuvent être lues au format attendu
# errors="coerce" : transforme date non convertible en NaT (NaT = valeur manquante après sum avec isna())
dates = pd.to_datetime(stations["date_mise_en_service"], format="%Y-%m-%d", errors="coerce")
print(f"\nNombre de dates invalides : {dates.isna().sum()}")

# Format attendu : AAAA-MM-JJ.
formats_dates_valides = stations["date_mise_en_service"].str.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", na=False)
print(f"\nDates dont le format n'est pas AAAA-MM-JJ : {(~formats_dates_valides).sum()}")

# RG1 : la capacité doit être un entier strictement positif
#si la conversion échoue, met NaN
#pd.to_numeric() : convertit les valeurs en nombres
capacites = pd.to_numeric(stations["capacite"], errors="coerce")
capacites_invalides = (capacites.isna() | (capacites <= 0) | (capacites % 1 != 0))
print(f"\nCapacités non numériques, non entières ou non positives : {capacites_invalides.sum()}")

# Les coordonnées doivent être numériques et présentes
for colonne in ["latitude", "longitude"]:
    valeurs = pd.to_numeric(stations[colonne], errors="coerce")
    print(f"\nValeurs non numériques ou absentes pour {colonne} : {valeurs.isna().sum()}")

#limite des latitudes et longitudes des coordonnées WGS84
    #après recherche -90<=latitude<=90  ET -180<=longitude<=180
latitudes = pd.to_numeric(stations["latitude"], errors="coerce")
longitudes = pd.to_numeric(stations["longitude"], errors="coerce")
print(f"\nLatitudes hors limites : {((latitudes < -90) | (latitudes > 90)).sum()}")
print(f"Longitudes hors limites : {((longitudes < -180) | (longitudes > 180)).sum()}")
# Relit les valeurs en texte pour conserver les décimales du CSV
stations_texte = pd.read_csv("data/stations.csv", dtype=str)
for colonne in ["latitude", "longitude"]:
    #-? autorise le signe -
    #[0-9]+ demande un ou plusieurs chiffres
    #\. demande un . réel
    #[0-9]{5} demande exactement 5 chiffres après le .
    formats_valides = stations_texte[colonne].str.fullmatch(r"-?[0-9]+\.[0-9]{5}", na=False)
    #print(stations_texte.loc[~formats_valides, ["station_id", colonne]])
    print(f"Coordonnées sans exactement cinq décimales pour {colonne} : {(~formats_valides).sum()}")


# Vérifie les textes obligatoires et leur longueur
for colonne in ["nom", "commune"]:
    #fillna("") : remplace les valeurs absentes par des chaines vides
    textes = stations[colonne].fillna("").astype(str)
    textes_vides = textes.str.strip() == ""
    textes_trop_longs = textes.str.len() > 100
    print(f"\nTextes vides pour {colonne} : {textes_vides.sum()}")
    print(f"Textes dépassant 100 caractères pour {colonne} : {textes_trop_longs.sum()}")


###########################################################################fin Stations###########################
###########################################################################trajets###########################
# Audit des trajets.
print("\n--- AUDIT DES TRAJETS ---")

trajets = pd.read_csv("data/trajets.csv")

print(trajets.head())
print(f"Nombre de lignes : {trajets.shape[0]}")
print(f"Nombre de colonnes : {trajets.shape[1]}")

print(f"\nValeurs manquantes : {trajets.isna().sum()}")

print(f"\nNombre de lignes dupliquées : {trajets.duplicated().sum()}")
print(f"Nombre d'identifiants répétés : {trajets['trajet_id'].duplicated().sum()}")

#value_counts(dropna=False) : compte tout même les valeurs absentes
print(f"\nTypes d'usagers : {trajets['type_usager'].value_counts(dropna=False)}")

# RG5 : pseudonyme attendu pour un abonné
abonnes_sans_reference = trajets[(trajets["type_usager"] == "abonne") & trajets["usager_ref"].isna()]
# RG5 : un occasionnel ne doit pas porter de pseudonyme
occasionnels_avec_reference = trajets[(trajets["type_usager"] == "occasionnel") & trajets["usager_ref"].notna()]
print(f"\nAbonnés sans pseudonyme : {len(abonnes_sans_reference)}")
print(f"Occasionnels avec un pseudonyme : {len(occasionnels_avec_reference)}")

#RG4 : durée entière et strictement positive
durees = pd.to_numeric(trajets["duree_secondes"], errors="coerce")
durees_invalides = (durees.isna() | (durees <= 0) | (durees % 1 != 0))
print(f"\nNombre de durées invalides : {durees_invalides.sum()}")
# Affiche les trajets concernés pour examiner le défaut
#loc affiche les lignes concernées et les deux colonnes utiles
print(trajets.loc[durees_invalides, ["trajet_id", "duree_secondes"]])

#stations de départ absentes ou inconnues
departs_invalides = ~trajets["station_depart"].isin(stations["station_id"])

#une station arrivée absente est autorisée 
arrivees_invalides = (trajets["station_arrivee"].notna() & ~trajets["station_arrivee"].isin(stations["station_id"]))
print(f"\nStations de départ absentes ou inconnues : {departs_invalides.sum()}")
print(trajets.loc[departs_invalides, ["trajet_id", "station_depart"]])
print(f"\nStations d'arrivée renseignées mais inconnues : {arrivees_invalides.sum()}")
print(trajets.loc[arrivees_invalides, ["trajet_id", "station_arrivee"]])

# Identifiant du trajet : T + 6 chiffres
trajet_id_valides = trajets["trajet_id"].str.fullmatch(r"T[0-9]{6}", na=False)
trajet_id_invalides = ~trajet_id_valides
print(f"\nIdentifiants de trajet au mauvais format : {trajet_id_invalides.sum()}")
print(trajets.loc[trajet_id_invalides, ["trajet_id"]])

# Identifiant du vélo : V + 4 chiffres
velo_id_valides = trajets["velo_id"].str.fullmatch(r"V[0-9]{4}", na=False)
velo_id_invalides = ~velo_id_valides
print(f"\nIdentifiants de vélo au mauvais format : {velo_id_invalides.sum()}")
print(trajets.loc[velo_id_invalides, ["trajet_id", "velo_id"]])

# Vérifie le format après passage en majuscules.
velo_id_majuscules = trajets["velo_id"].str.upper()
velo_id_valides_apres_correction = velo_id_majuscules.str.fullmatch(r"V[0-9]{4}", na=False)
print(f"\nIdentifiants de vélo encore invalides après passage en majuscules : {(~velo_id_valides_apres_correction).sum()}")

# Format attendu du pseudonyme lorsqu'il est présent.
references_valides = trajets["usager_ref"].str.fullmatch(
    r"U[0-9A-Fa-f]{8}", na=False
)

# une référence absente n'est pas comptée comme un mauvais format
references_invalides = (trajets["usager_ref"].notna() & ~references_valides)
print(f"\nPseudonymes renseignés au mauvais format : {references_invalides.sum()}")
print(trajets.loc[references_invalides, ["trajet_id", "usager_ref"]])

#format attendu : AAAA-MM-JJ HH:MM:SS
formats_depart_valides = trajets["depart_horodatage"].str.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}", na=False)
print(f"\nDates de départ au mauvais format : {(~formats_depart_valides).sum()}")
print(trajets.loc[~formats_depart_valides, ["trajet_id", "depart_horodatage"]])

#dates au format attendu
dates_depart = pd.to_datetime(trajets["depart_horodatage"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
#dates au format français
dates_depart_fr = pd.to_datetime(trajets["depart_horodatage"], format="%d/%m/%Y %H:%M", errors="coerce")
#des dates au format français
dates_depart = dates_depart.fillna(dates_depart_fr)
print(f"\nDates de départ impossibles ou non reconnues : {dates_depart.isna().sum()}")
print(trajets.loc[dates_depart.isna(), ["trajet_id", "depart_horodatage"]])

#copie sans les doublons de lignes identiques
trajets_sans_doublons = trajets.drop_duplicates()
print(f"\nNombre de lignes après retrait des doublons : {len(trajets_sans_doublons)}")
#les identifiaints sont bein unique après ça :
print(f"Identifiants encore répétés après retrait des doublons : {trajets_sans_doublons["trajet_id"].duplicated().sum()}")

#controles sur les lignes sans doublons
durees_uniques = pd.to_numeric(trajets_sans_doublons["duree_secondes"], errors="coerce")
durees_invalides_uniques = (durees_uniques.isna() | (durees_uniques <= 0) | (durees_uniques % 1 != 0))
departs_invalides_uniques = ~trajets_sans_doublons["station_depart"].isin(stations["station_id"])
arrivees_invalides_uniques = (trajets_sans_doublons["station_arrivee"].notna() & ~trajets_sans_doublons["station_arrivee"].isin(stations["station_id"]))
# ligne est comptée une seule fois, même avec plusieurs défauts.
lignes_a_rejeter = (durees_invalides_uniques | departs_invalides_uniques | arrivees_invalides_uniques)
print(f"\nLignes à rejeter pour durée ou station invalide : {lignes_a_rejeter.sum()}")
print(f"Lignes restantes après ces contrôles : {(~lignes_a_rejeter).sum()}")

###########################################################################fin Stations###########################
###########################################################################trajets###########################
# Audit des incidents.
print("\n--- AUDIT DES INCIDENTS ---")

incidents = pd.read_csv("data/incidents.csv")

print(incidents.head())
print(f"Nombre de lignes : {incidents.shape[0]}")
print(f"Nombre de colonnes : {incidents.shape[1]}")

print(f"\nValeurs manquantes : {incidents.isna().sum()}")

print(f"\nNombre de lignes dupliquées : {incidents.duplicated().sum()}")

print(f"Nombre d'identifiants répétés : { incidents["incident_id"].duplicated().sum()}")

# RG7 : observer les différentes écritures des statuts
print(f"\nStatuts présents dans le CSV : {incidents["statut"].value_counts(dropna=False)}")

"""Ouvert et ouvert 
En cours, en cours et en_cours 
RESOLU, Resolu et resolu."""
#status en minuscules et remplace espace par underscore
statuts_normalises = (
    incidents["statut"]
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False))

print(f"\nStatuts après normalisation : {statuts_normalises.value_counts(dropna=False)}")

print(f"\nNombre de statuts à normaliser : {(incidents["statut"] != statuts_normalises).sum()}")

# RG7 : seuls ces trois statuts sont autorisés.
statuts_invalides = ~statuts_normalises.isin(["ouvert", "en_cours", "resolu"])

print(f"\nStatuts invalides après normalisation : {statuts_invalides.sum()}")

print(incidents.loc[statuts_invalides, ["incident_id", "statut"]])

# RG6 : observer les cibles présentes
print(f"\nCibles présentes dans le CSV : {incidents["cible"].value_counts(dropna=False)}")

#RG6 : un incident vélo doit avoir uniquement une référence vélo
incidents_velo_invalides = ((incidents["cible"] == "velo")
    & (incidents["velo_id"].isna() | incidents["station_id"].notna()))
print(f"\nIncidents vélo avec des références incorrectes : {incidents_velo_invalides.sum()}")
print(incidents.loc[incidents_velo_invalides, ["incident_id", "cible", "velo_id", "station_id"]])

# RG6 : un incident station doit avoir uniquement une référence station
incidents_station_invalides = ((incidents["cible"] == "station")
    & (incidents["station_id"].isna() | incidents["velo_id"].notna()))
print(f"\nIncidents station avec des références incorrectes : {incidents_station_invalides.sum()}")
print(incidents.loc[incidents_station_invalides, ["incident_id", "cible", "velo_id", "station_id"]])

# RG6 : une station concernée doit exister dans le référentiel
stations_incidents_inconnues = (incidents["station_id"].notna()
    & ~incidents["station_id"].isin(stations["station_id"]))
print(f"\nIncidents avec une station inconnue : {stations_incidents_inconnues.sum()}")
print(incidents.loc[stations_incidents_inconnues, ["incident_id", "station_id"]])

#format attendu : I2026- + 4 chiffres
incident_id_valides = incidents["incident_id"].str.fullmatch(r"I2026-[0-9]{4}", na=False)
incident_id_invalides = ~incident_id_valides
print(f"\nIdentifiants d'incident au mauvais format : {incident_id_invalides.sum()}")
print(incidents.loc[incident_id_invalides, ["incident_id"]])

# Format attendu du vélo : V suivi de quatre chiffres.
velos_incidents_valides = incidents["velo_id"].str.fullmatch(r"V[0-9]{4}", na=False)
velos_incidents_invalides = (incidents["velo_id"].notna() & ~velos_incidents_valides)
print(f"\nIdentifiants de vélo avec mauvais format : {velos_incidents_invalides.sum()}")
print(incidents.loc[velos_incidents_invalides, ["incident_id", "velo_id"]])

# RG8 : un incident résolu doit avoir une date de résolution
resolus_sans_date = ((statuts_normalises == "resolu") & incidents["date_resolution"].isna())
print(f"\nIncidents résolus sans date de résolution : {resolus_sans_date.sum()}")
print(incidents.loc[resolus_sans_date, ["incident_id", "statut", "date_resolution"]])

# RG8 : un incident non résolu ne doit pas avoir de date de résolution
non_resolus_avec_date = ((statuts_normalises != "resolu") & incidents["date_resolution"].notna())
print(f"\nIncidents non résolus avec une date de résolution : {non_resolus_avec_date.sum()}")
print(incidents.loc[non_resolus_avec_date, ["incident_id", "statut", "date_resolution"]])

# Date de signalement attendue : AAAA-MM-JJ HH:MM
dates_signalement = pd.to_datetime(incidents["date_signalement"], format="%Y-%m-%d %H:%M", errors="coerce")
print(f"\nDates de signalement impossibles ou non reconnues : {dates_signalement.isna().sum()}")
print(incidents.loc[dates_signalement.isna(), ["incident_id", "date_signalement"]])

# Date de résolution attendue : AAAA-MM-JJ HH:MM
dates_resolution = pd.to_datetime(incidents["date_resolution"], format="%Y-%m-%d %H:%M", errors="coerce")

# Une date absente est autorisée pour un incident non résolu
dates_resolution_invalides = (incidents["date_resolution"].notna() & dates_resolution.isna())
print(f"\nDates de résolution renseignées mais impossibles ou non reconnues : {dates_resolution_invalides.sum()}")
print(incidents.loc[dates_resolution_invalides, ["incident_id", "date_resolution"]])

# RG8 : pas date résolution avant date signalement
resolutions_avant_signalement = (dates_resolution.notna() & dates_signalement.notna() & (dates_resolution < dates_signalement))
print(f"\nDates de résolution antérieures au signalement : {resolutions_avant_signalement.sum()}")
print(incidents.loc[resolutions_avant_signalement, ["incident_id", "date_signalement", "date_resolution"]])

# RG8 : technicien attendu pour un incident en cours ou résolu
techniciens_manquants = (statuts_normalises.isin(["en_cours", "resolu"]) & (incidents["technicien"].fillna("").str.strip() == ""))
print(f"\nIncidents pris en charge sans technicien : {techniciens_manquants.sum()}")
print(incidents.loc[techniciens_manquants, ["incident_id", "statut", "technicien"]])

# Catégories prévues dans README-donnees.md
types_autorises = [
    "vandalisme",
    "selle abimee",
    "eclairage HS",
    "chaine deraillee",
    "ecran borne illisible",
    "pneu creve",
    "frein defectueux",
    "borne hors service"]
types_incident_invalides = ~incidents["type_incident"].isin(types_autorises)
print(f"\nTypes d'incident absents ou non reconnus : {types_incident_invalides.sum()}")
print(incidents.loc[types_incident_invalides, ["incident_id", "type_incident"]])

# Format attendu : AAAA-MM-JJ HH:MM
formats_signalement_valides = incidents["date_signalement"].str.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}", na=False)
print(f"\nDates de signalement au mauvais format : {(~formats_signalement_valides).sum()}")
print(incidents.loc[~formats_signalement_valides, ["incident_id", "date_signalement"]])

# Format attendu : AAAA-MM-JJ HH:MM
formats_resolution_valides = incidents["date_resolution"].str.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}", na=False)
formats_resolution_invalides = (incidents["date_resolution"].notna() & ~formats_resolution_valides)
print(f"\nDates de résolution renseignées au mauvais format : {formats_resolution_invalides.sum()}")
print(incidents.loc[formats_resolution_invalides, ["incident_id", "date_resolution"]])

#type incident obligatoire et limité à 100 caractères
types_textes = incidents["type_incident"].fillna("").astype(str)
print(f"\nTypes d'incident vides : {(types_textes.str.strip() == "").sum()}")
print(f"Types d'incident dépassant 100 caractères : {(types_textes.str.len() > 100).sum()}")

# Le technicien peut être absent, mais son nom est limité à 100 caractères
techniciens_textes = incidents["technicien"].fillna("").astype(str)
print(f"Noms de technicien dépassant 100 caractères : {(techniciens_textes.str.len() > 100).sum()}")

# Une ligne est rejetée si au moins un contrôle bloquant échoue
incidents_a_rejeter = (statuts_invalides
                        | incidents_velo_invalides
                        | incidents_station_invalides
                        | stations_incidents_inconnues
                        | incident_id_invalides
                        | velos_incidents_invalides
                        | resolus_sans_date
                        | non_resolus_avec_date
                        | dates_signalement.isna()
                        | dates_resolution_invalides
                        | resolutions_avant_signalement
                        | types_incident_invalides
                        | (types_textes.str.strip() == "")
                        | (types_textes.str.len() > 100)
                        | (techniciens_textes.str.len() > 100))
print(f"\nIncidents à rejeter : {incidents_a_rejeter.sum()}")
print(f"Incidents restants : {(~incidents_a_rejeter).sum()}")
