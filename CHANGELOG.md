# Journal des versions

Une section par version, avec les changements regroupés en
« Ajouté », « Modifié », « Corrigé ».

## [Non livré]

### Ajouté
- Fonction de normalisation des statuts d’incident (normaliser_statut).
- Tests unitaires des statuts valides, à normaliser, inconnus et absents.
- Fonction de normalisation et de contrôle des identifiants de vélo.
- Tests unitaires des identifiants de vélo.
- Fonction de conversion et de contrôle des entiers strictement positifs.
- Tests unitaires des capacités et durées : valeurs valides, nulles, négatives, décimales, non numériques et absentes.
- Fonction de conversion des dates de mise en service des stations.
- Tests des dates valides, impossibles, absentes et au mauvais format.
- Conversion des horodatages des trajets et incidents (format français aussi repéré dans les CSV).
- Tests des formats acceptés et des horodatages invalides.
- Contrôle de cohérence entre le statut et les dates des incidents.
- Tests des dates de résolution présentes, absentes et antérieures ou égales au signalement.
- Contrôle de la cible des incidents et de leurs références vélo/station.
- Tests des cibles valides, inconnues et des références incohérentes.
- Contrôle des références aux stations existantes.
- Tests des références connues, inconnues, absentes et du référentiel vide.
- Normalisation des champs textuels facultatifs.
- Tests des valeurs présentes, absentes, vides et composées d’espaces.
- Contrôle des textes obligatoires et de leur longueur maximale.
- Tests des textes valides, absents, vides et trop longs.
- Normalisation et contrôle du format des identifiants de station.
- Tests des identifiants de station valides, à normaliser et invalides.
- Normalisation et contrôle du format des identifiants de trajet.
- Tests des identifiants de trajet valides, à normaliser et invalides.
- Normalisation et contrôle du format des identifiants d’incident.
- Tests des identifiants d’incident valides, à normaliser et invalides.
- Normalisation et contrôle du type d’usager des trajets.
- Tests des types abonne et occasionnel, des corrections et des valeurs refusées.
- Contrôle du format des pseudonymes d’usager lorsqu’ils sont renseignés.
- Tests des pseudonymes valides, absents et au mauvais format.
- Contrôle du pseudonyme selon le type d’usager.
- Tests des cas acceptés, du rejet pour un occasionnel avec pseudonyme et de l’avertissement pour un abonné sans pseudonyme.
- Signalement des techniciens absents pour les incidents en cours ou résolus.
- Tests des avertissements liés à l’absence de technicien.
- Contrôle des catégories d’incident autorisées.
- Tests des catégories valides, inconnues, absentes et vides.
- Conversion des coordonnées des stations et contrôle des limites géographiques.
- Tests des coordonnées valides, absentes, non numériques et hors limites.
- Normalisation des cibles vélo et station des incidents.
- Tests des cibles valides, à normaliser, inconnues et absentes.
- Séparation des lignes uniques et des doublons strictement identiques.
- Tests des répétitions, des lignes différentes et de la liste vide.
- Lecture des trois CSV avec Pandas dans scripts/importer.py.
- Séparation des doublons de trajets avec la fonction `separer_doublons` déjà testée.
- Fiabilisation des stations avec les fonctions testées.
- Création du journal d’import et traçabilité des doublons de trajets.


## [0.0.2] - 2026-10-14

### Ajouté
- Tables station, trajet, incident et utilisateur avec leurs contraintes.
- Index pour les filtres et les indicateurs.
- Documentation du modèle de données et des règles RG1 à RG8.
- Script d’audit des exports CSV.
- Résultats de l’audit des stations dans docs/schema-donnees.md.
- Résultats de l’audit des trajets dans docs/schema-donnees.md.
- Résultats de l’audit des incidents dans docs/schema-donnees.md.
- Conclusion de l'audit dans docs/schema-donnees.md.
- Vérifications manuelles des contraintes SQL dans pgAdmin, avec résultats documentés dans schema-donnees.md et transactions annulées par ROLLBACK.
- Requêtes de vérification du schéma gardées dans sql/verifications_schema.sql.

### Modifié
- README complété avec la création des tables et le chargement des comptes.
- Procédure de correction du propriétaire des tables documentée dans le README.md (avant : postgres. Après : veloville).

## [0.0.1] - 2026-10-13

### Ajouté
- Script de génération du secret JWT.
- Chargement de la configuration depuis le fichier .env.
- Connexion PostgreSQL avec SQLAlchemy.
- Test d’intégration de la connexion PostgreSQL.
- Documentation de préparation de l’environnement dans le README.

### Modifié
- Versions des dépendances fixées dans requirements.txt.

### Corrigé
- Encodage de requirements.txt converti en UTF-8.

## [0.0.0] - 2026-10-13

### Ajouté
- Initialisation du projet à partir du squelette fourni.
- Version identifiée par le tag v0.0.0.