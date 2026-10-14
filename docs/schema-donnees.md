# Schéma de données

Le schéma est défini dans `sql/schema.sql`.

Il s’appuie sur le contrat technique du sujet,
le cahier des charges de référence et le dictionnaire
`README-donnees.md`.

## 1. Modèle logique des données

Les clés primaires sont soulignées.
Les clés étrangères sont précédées de #.

station (<u>`station_id`</u>, `nom`, `commune`, `capacite`, `latitude`, `longitude`, `date_mise_en_service`)

trajet (<u>`trajet_id`</u>, `velo_id`, `depart_horodatage`, `#station_depart`, `#station_arrivee`, `duree_secondes`, `type_usager`, `usager_ref`)

incident (<u>`incident_id`</u>, `date_signalement`, `cible`, `velo_id`, `#station_id`, `type_incident`, `statut`, `date_resolution`, `technicien`)

utilisateur (<u>`id_utilisateur`</u>, `username`, `mot_de_passe_hash`, `role`)

Les clés étrangères `station_depart`, `station_arrivee` et `incident.station_id` font référence à `station.station_id`.

Les champs pouvant être absents et les autres contraintes sont précisés dans la description des tables.

## 2. Description des tables et contraintes

### station

Référentiel des stations.

| Colonne | Type | Contraintes |
|---|---|---|
| `station_id` | VARCHAR(10) | PK, format S suivi de 3 chiffres |
| `nom` | VARCHAR(100) | NOT NULL |
| `commune` | VARCHAR(100) | NOT NULL |
| `capacite` | INTEGER | NOT NULL, strictement positive |
| `latitude` | NUMERIC(8,5) | NOT NULL |
| `longitude` | NUMERIC(8,5) | NOT NULL |
| `date_mise_en_service` | DATE | NOT NULL |

### trajet

Locations de vélos.

| Colonne | Type | Contraintes |
|---|---|---|
| `trajet_id` | VARCHAR(12) | PK, format T suivi de 6 chiffres |
| `velo_id` | VARCHAR(8) | NOT NULL, format V suivi de 4 chiffres |
| `depart_horodatage` | TIMESTAMP | NOT NULL |
| `station_depart` | VARCHAR(10) | NOT NULL, FK vers station |
| `station_arrivee` | VARCHAR(10) | NULL autorisé, FK vers station |
| `duree_secondes` | INTEGER | NOT NULL, strictement positive |
| `type_usager` | VARCHAR(20) | NOT NULL, abonne ou occasionnel |
| `usager_ref` | VARCHAR(9) | NULL autorisé, U suivi de 8 caractères hexadécimaux|

Un usager occasionnel ne doit pas porter de pseudonyme : `usager_ref` doit être NULL.

### incident

Signalements de maintenance.

| Colonne | Type | Contraintes |
|---|---|---|
| `incident_id` | VARCHAR(12) | PK, format I2026- suivi de 4 chiffres |
| `date_signalement` | TIMESTAMP | NOT NULL |
| `cible` | VARCHAR(20) | NOT NULL, velo ou station |
| `velo_id` | VARCHAR(8) | NULL autorisé, format V suivi de 4 chiffres si renseigné |
| `station_id` | VARCHAR(10) | NULL autorisé, FK vers station |
| `type_incident` | VARCHAR(100) | NOT NULL, catégorie parmi les huit valeurs du dictionnaire |
| `statut` | VARCHAR(20) | NOT NULL, ouvert, en_cours ou resolu |
| `date_resolution` | TIMESTAMP | NULL autorisé selon le statut |
| `technicien` | VARCHAR(100) | NULL autorisé |

Catégories autorisées :
- vandalisme ;
- selle abimee ;
- eclairage HS ;
- chaine deraillee ;
- ecran borne illisible ;
- pneu creve ;
- frein defectueux ;
- borne hors service.

La contrainte `ck_incident_cible` impose :
- cible velo : `velo_id` renseigné et `station_id` NULL,
- cible station : `station_id` renseigné et `velo_id` NULL.

La contrainte `ck_incident_resolution` impose :
- statut resolu : `date_resolution` renseignée et supérieure ou égale à `date_signalement`,
- autre statut : `date_resolution` NULL.

### utilisateur

Comptes d’authentification de l’application.

| Colonne | Type | Contraintes |
|---|---|---|
| `id_utilisateur` | SERIAL | PK, identifiant généré automatiquement |
| `username` | VARCHAR(100) | NOT NULL, UNIQUE |
| `mot_de_passe_hash` | TEXT | NOT NULL |
| `role` | VARCHAR(20) | NOT NULL, exploitant ou direction |

Les mots de passe sont stockés sous forme de hachages bcrypt. Les deux comptes de recette sont fournis dans `sql/comptes.sql`.

## 3. Correspondance avec les règles de gestion

| Règle | Contrôle dans le schéma | Contrôle complémentaire à développer |
|---|---|---|
| RG1 | Chaque station possède un identifiant unique. Sa capacité est un entier strictement positif. | À l’import, corriger les valeurs lorsque la bonne valeur est certaine. Rejeter les lignes qui restent incorrectes et noter la raison dans le journal. |
| RG2 | La station de départ est obligatoire et doit exister. La station d’arrivée doit exister lorsqu’elle est renseignée. | Vérifier les stations indiquées dans les CSV avant d’enregistrer les trajets. Rejeter les références erronées et noter la raison dans le journal. |
| RG3 | La station d’arrivée peut être absente : `station_arrivee` accepte NULL. | Conserver le trajet avec une arrivée absente, sans inventer de station. Ne pas le compter comme une arrivée dans les indicateurs. |
| RG4 | La durée du trajet est un entier strictement positif, exprimé en secondes. | Vérifier les durées dans le CSV. Rejeter les durées incorrectes et noter la raison dans le journal. |
| RG5 | Le type d’usager est `abonne` ou `occasionnel`. Le pseudonyme respecte le format attendu lorsqu’il est renseigné. Un occasionnel ne porte pas de pseudonyme. | Vérifier le lien entre le type d’usager et le pseudonyme. Signaler un pseudonyme absent pour un abonné, sans inventer de valeur. Le contrat technique autorise ce champ à être absent. |
| RG6 | Un incident concerne un vélo ou une station, jamais les deux ni aucun. La référence renseignée correspond à la cible. Une station concernée doit exister. | Vérifier la cible et les références dans le CSV. Rejeter les lignes incorrectes et noter la raison dans le journal. |
| RG7 | Le statut est `ouvert`, `en_cours` ou `resolu`. | Corriger les différences d’écriture des statuts à l’import. Dans l’API, autoriser seulement `ouvert --> en_cours`, `ouvert --> resolu` et `en_cours --> resolu`. Un incident résolu ne change plus de statut. |
| RG8 | La date de résolution est présente uniquement pour un incident résolu. Elle ne peut pas être antérieure au signalement. Le technicien peut être absent. | Corriger les formats de dates lorsque c’est possible. Rejeter les dates incohérentes. Signaler l’absence de technicien dès la prise en charge, sans empêcher l’enregistrement. |


## 4. Index

| Index | Utilité |
|---|---|
| `idx_station_commune` | Filtre des stations par commune |
| `idx_trajet_depart_horodatage` | Filtre des trajets par période |
| `idx_trajet_station_depart` | Recherche par station et calcul des départs |
| `idx_trajet_station_arrivee` | Recherche par station et calcul des arrivées |
| `idx_incident_statut_date` | Filtre par statut et tri par date décroissante |


## 5. Création et droits d’accès

Exécuter dans cet ordre :
1. `sql/schema.sql`,
2. `sql/comptes.sql`.

Pour une nouvelle installation, exécuter les scripts dans la base veloville avec le rôle PostgreSQL veloville.

Les droits SELECT, INSERT et UPDATE du rôle veloville ont été vérifiés sur les quatre tables.

## 6. Vérifications réalisées

| Vérification | Résultat obtenu |
|---|---|
| Première exécution de schema.sql | Tables et index créés |
| Seconde exécution de schema.sql | Aucune erreur, éléments existants conservés |
| Chargement des comptes | exploitant01 et direction01 présents avec les rôles attendus |
| Permissions du rôle veloville | SELECT, INSERT et UPDATE accordés sur les quatre tables |
| Test automatisé de connexion | 1 passed |
| Station avec capacité 0 | Refusée par `station_capacite_check` |
| Station avec capacité 15 | Acceptée |
| Trajet avec station de départ inexistante | Refusé par `fk_trajet_station_depart` |
| Trajet avec départ existant et arrivée NULL | Accepté |
| Trajet avec durée 0 | Refusé par `trajet_duree_secondes_check` |
| Incident visant un vélo et une station | Refusé par `ck_incident_cible` |
| Incident ouvert visant uniquement un vélo, sans technicien | Accepté |
| Résolution antérieure au signalement | Refusée par `ck_incident_resolution` |
| Résolution égale au signalement | Acceptée |
| Incident résolu sans date de résolution | Refusé par `ck_incident_resolution` |
| Incident ouvert avec date de résolution | Refusé par `ck_incident_resolution` |

Les insertions de vérification ont été exécutées dans des transactions annulées avec ROLLBACK : aucune donnée de test n’est conservée.

CREATE TABLE IF NOT EXISTS permet de relancer la création, mais ne modifie pas une table déjà existante.

Ces vérifications couvrent les cas indiqués dans le tableau, pas toutes les contraintes du schéma.

Les requêtes de vérification sont conservées dans `sql/verifications_schema.sql`. Chaque cas est exécuté séparément.

## 7. Audit des données

L’audit est réalisé avec `scripts/audit_donnees.py`,
avant le chargement des CSV dans PostgreSQL.
Les fichiers sources ne sont pas modifiés.

### stations.csv

Le fichier contient 120 lignes et 7 colonnes.

| Contrôle réalisé | Nombre de lignes concernées | Traitement retenu |
|---|---:|---|
| Valeur manquante dans un champ obligatoire | 0 | Aucune correction nécessaire |
| Ligne strictement identique à une précédente | 0 | Aucun doublon à écarter |
| Identifiant de station répété | 0 | Aucune correction nécessaire |
| Identifiant ne respectant pas S suivi de 3 chiffres | 0 | Aucune correction nécessaire |
| Capacité non numérique, non entière ou non positive | 0 | Aucune correction nécessaire |
| Date de mise en service impossible ou absente | 0 | Aucune correction nécessaire |
| Date ne respectant pas le format AAAA-MM-JJ | 0 | Aucune correction nécessaire |
| Latitude absente ou non numérique | 0 | Aucune correction nécessaire |
| Longitude absente ou non numérique | 0 | Aucune correction nécessaire |
| Nom vide ou composé uniquement d’espaces | 0 | Aucune correction nécessaire |
| Commune vide ou composée uniquement d’espaces | 0 | Aucune correction nécessaire |
| Nom dépassant 100 caractères | 0 | Aucune correction nécessaire |
| Commune dépassant 100 caractères | 0 | Aucune correction nécessaire |
| Latitude écrite avec moins de cinq décimales | 17 | Conserver. Stockage avec cinq décimales dans NUMERIC(8,5), sans changer la valeur |
| Longitude écrite avec moins de cinq décimales | 11 | Conserver. Stockage avec cinq décimales dans NUMERIC(8,5), sans changer la valeur |
| Latitude hors des limites -90 à 90 | 0 | Aucune correction nécessaire |
| Longitude hors des limites -180 à 180 | 0 | Aucune correction nécessaire |


Bilan prévisionnel :
120 lignes conservées + 0 rejet + 0 doublon écarté = 120 lignes.

Les coordonnées écrites avec moins de cinq décimales sont conservées :
leur stockage dans NUMERIC(8,5) ne change pas leur valeur.

Ces résultats seront confirmés lors de l’import.
Aucune station n’a encore été chargée dans PostgreSQL.

### trajets.csv

Le fichier contient 2 030 lignes et 8 colonnes.
Les comptages ci-dessous portent sur le CSV brut, sauf indication contraire.

| Défaut ou contrôle | Nombre de lignes concernées | Traitement retenu |
|---|---:|---|
| Répétitions de lignes identiques | 12 | Conserver une seule occurrence et journaliser les doublons écartés |
| Identifiants encore répétés après retrait des doublons | 0 | Aucune correction nécessaire |
| Durée nulle ou négative | 10 dans le CSV brut, 9 après retrait des doublons | Rejeter et journaliser |
| Station de départ absente ou inconnue | 0 | Aucune correction nécessaire |
| Station d’arrivée renseignée mais inconnue : S999 | 7 | Rejeter et journaliser, ne pas remplacer par NULL |
| Station d’arrivée absente | 23 | Conserver avec NULL, conformément à RG3 |
| Identifiant de trajet au mauvais format | 0 | Aucune correction nécessaire |
| Identifiant de vélo avec un v minuscule | 6 | Passer en majuscules et journaliser la normalisation |
| Identifiant de vélo encore invalide après passage en majuscules | 0 | Aucune autre correction nécessaire |
| Type d’usager différent de abonne ou occasionnel | 0 | Aucune correction nécessaire |
| Abonné sans pseudonyme | 0 | Aucune correction nécessaire |
| Occasionnel avec un pseudonyme | 0 | Aucune correction nécessaire |
| Pseudonyme renseigné au mauvais format | 0 | Aucune correction nécessaire |
| Date de départ au format JJ/MM/AAAA HH:MM | 5 | Convertir au format attendu, avec secondes à 00, journaliser la normalisation |
| Date impossible ou non reconnue après lecture des deux formats | 0 | Aucune |

Après retrait des 12 doublons, il reste 2 018 lignes.
Parmi elles, 16 présentent une durée invalide ou une station inconnue.
Il reste donc 2 002 lignes après ces contrôles.

Bilan prévisionnel :
2 002 lignes conservées + 16 rejets + 12 doublons écartés = 2 030 lignes.

Une ligne peut présenter plusieurs défauts. Les nombres de défauts
ne doivent donc pas être additionnés pour calculer les rejets.

Par exemple, T480152 possède une date au format français et une arrivée
S999 : la date peut être corrigée, mais la ligne reste à rejeter
pour sa station inconnue.

Ces résultats sont des prévisions à confirmer lors de l’import.
Aucun trajet n’a encore été chargé dans PostgreSQL.

### incidents.csv

Le fichier contient 180 lignes et 9 colonnes.
Les comptages portent sur le CSV brut.

| Défaut ou contrôle | Nombre de lignes concernées | Traitement retenu |
|---|---:|---|
| Lignes identiques ou identifiants répétés | 0 | Aucun doublon à écarter |
| Statut écrit différemment du format attendu | 125 | Normaliser en ouvert, en_cours ou resolu et journaliser |
| Statut inconnu après normalisation | 0 | Aucune correction nécessaire |
| Cible différente de velo ou station | 0 | Aucune correction nécessaire |
| Références vélo/station incohérentes avec la cible | 0 | Aucune correction nécessaire |
| Station renseignée mais inconnue | 0 | Aucune correction nécessaire |
| Identifiant d’incident au mauvais format | 0 | Aucune correction nécessaire |
| Identifiant de vélo renseigné au mauvais format | 0 | Aucune correction nécessaire |
| Incident résolu sans date de résolution | 0 | Aucune correction nécessaire |
| Incident non résolu avec une date de résolution | 0 | Aucune correction nécessaire |
| Date de signalement impossible ou au mauvais format | 0 | Aucune correction nécessaire |
| Date de résolution renseignée impossible ou au mauvais format | 0 | Aucune correction nécessaire |
| Résolution antérieure au signalement | 3 | Rejeter et journaliser, sans inventer une date corrigée |
| Technicien absent pour un incident en cours ou résolu | 25 | Signaler dans le journal sans rejeter pour ce motif |
| Type d’incident absent ou non reconnu | 0 | Aucune correction nécessaire |
| Type d’incident ou nom de technicien dépassant 100 caractères | 0 | Aucune correction nécessaire |

Les incidents à rejeter sont I2026-0028, I2026-0124 et I2026-0178.

Après normalisation, nous avons :
55 ouvert, 46 en_cours et 79 resolu.
Ces nombres incluent les incidents qui seront rejetés.

Bilan prévisionnel :
177 lignes conservées + 3 rejets + 0 doublon écarté = 180 lignes.

Les normalisations et avertissements ne sont pas des rejets.
Une ligne peut recevoir plusieurs messages dans le journal.

Ces résultats seront confirmés lors de l’import.
Aucun incident n’a encore été chargé dans PostgreSQL.

### Conclusion de l’audit

Les trois exports CSV ont été examinés avec Python et Pandas,
à l’aide du script `scripts/audit_donnees.py`, sans modifier
les fichiers sources ni charger leurs données dans PostgreSQL.

L’audit a permis de repérer les doublons, les valeurs à normaliser,
les lignes à rejeter et les informations absentes autorisées.

Après application des traitements prévus, les volumes attendus sont :
- 120 stations ;
- 2 002 trajets ;
- 177 incidents.

Ces volumes seront vérifiés après l’import. Les doublons écartés,
les rejets, les normalisations et les avertissements seront journalisés.
