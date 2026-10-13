"""Audit des exports CSV avant leur import dans PostgreSQL"""

import pandas as pd

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
    
    print(stations_texte.loc[
        ~formats_valides, ["station_id", colonne]
    ])
    
    print(f"Coordonnées sans exactement cinq décimales pour {colonne} : {(~formats_valides).sum()}")


# Vérifie les textes obligatoires et leur longueur
for colonne in ["nom", "commune"]:
    #fillna("") : remplace les valeurs absentes par des chaines vides
    textes = stations[colonne].fillna("").astype(str)
    textes_vides = textes.str.strip() == ""
    textes_trop_longs = textes.str.len() > 100
    print(f"\nTextes vides pour {colonne} : {textes_vides.sum()}")
    print(f"Textes dépassant 100 caractères pour {colonne} : {textes_trop_longs.sum()}")