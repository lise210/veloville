# Journal des versions

Une section par version, avec les changements regroupés en
« Ajouté », « Modifié », « Corrigé ».

## [Non livré]

### Ajouté
- Procédure d’installation locale, configuration PostgreSQL, import, lancement de l’API et de Streamlit, et vérifications après déploiement.


## [0.0.8] - 2026-10-15

### Ajouté
- Trois tests unitaires des réponses des indicateurs avec résultats SQL simulés.
- Dépendance pytest-mock pour les simulations dans les tests.

### Modifié
- Résultat global : 173 tests réussis, couverture des services de 95 %.

## [0.0.7] - 2026-10-15

### Ajouté
- Matrice des droits par route pour les accès anonymes, exploitant et direction.
- Relevé initial de recette : 8 cas OK et 2 cas KO.
- Fiches ANO-001 et ANO-002 concernant les messages HTTP 403 et 404.
- ANO-001 : message 403 aligné sur le texte attendu dans REC-06.
- ANO-002 : message 404 aligné sur le texte attendu dans REC-08.
- Tests de non-régression vérifiés : 170 tests réussis, couverture des services de 95 %.
- Rejeux de REC-06 et REC-08 réussis sur babea35.
- Anomalies ANO-001 et ANO-002 fermées après vérification.

## [0.0.6] - 2026-10-15

### Ajouté
- Client HTTP centralisé avec jeton Bearer, délai maximal et messages d’erreur en français.
- Gestion de la session Streamlit et formulaire de connexion.
- Vérifications manuelles : connexion réussie, mauvais mot de passe et API arrêtée.
- Identifiant, rôle et bouton de déconnexion dans la barre latérale.
- Page Stations protégée avec tableau, filtre par commune et pagination.
- Liste des communes mise en cache pendant une heure.
- Messages de chargement, d’absence de résultat et d’erreur.
- Page Incidents avec filtre par statut, pagination et tableau.
- Formulaire de changement de statut réservé à l’exploitant.
- Vérification manuelle sur un incident temporaire : passage de `ouvert` à `en_cours`, puis à `resolu` avec date de résolution automatique. Incident temporaire supprimé après vérification.
- Page Indicateurs avec sélection de période et nombre de stations.
- Trois métriques et trois tableaux.
- Vérifications manuelles des résultats, du filtre de dates et d’une période sans trajet.

### Corrigé
- Restauration de l’état initial d’un incident modifié pendant les essais manuels. Vérification complète : 169 tests réussis, couverture des services de 95 %.

## [0.0.5] - 2026-10-15

### Ajouté
- Modèle ORM Utilisateur.
- Vérification des mots de passe avec bcrypt et gestion des JWT.
- Dépendances d’authentification et de contrôle des rôles.
- Route POST /auth/login et schémas de connexion.
- Application FastAPI et route GET /sante.
- Fixture TestClient et cinq tests d’API : santé, connexion des deux rôles, refus d’un mauvais mot de passe et d’un compte inconnu.
- Route GET /stations/{station_id}, accessible aux deux rôles authentifiés.
- Tests des accès sans jeton, avec jeton invalide et avec les deux rôles.
- Fixtures fournissant les jetons exploitant et direction.
- Route GET /stations avec filtre par commune et pagination côté serveur.
- Taille de page par défaut de 20, bornée entre 1 et 100.
- Tests de pagination, du filtre par commune et du refus des paramètres hors limites.
- Route GET /trajets protégée, avec pagination et filtres par dates et station de départ ou d’arrivée.
- Tests de pagination par défaut, des filtres et du refus d’accès sans jeton.
- Route GET /incidents protégée, avec filtre par statut et pagination.
- Tri des incidents du plus récent au plus ancien.
- Tests de pagination, du filtre par statut et du refus d’accès sans jeton.
- Route PUT /incidents/{`incident_id`}/statut réservée au rôle exploitant.
- Contrôle des transitions autorisées et renseignement de la date de résolution.
- Tests du refus de modification sans connexion (401) et avec le rôle direction (403).
- Trois routes d’indicateurs protégées : activité par jour, stations actives et incidents par statut avec délai moyen de résolution.
- Schémas de réponse et tests des trois routes sur les données importées.

### Modifié
- README actualisé : 169 tests réussis et couverture des services de 95 %.

## [0.0.4] - 2026-10-14

### Ajouté
- Indicateur d’activité par jour, calculé dans PostgreSQL avec SQLAlchemy.
- Tests d’intégration des comptages, des bornes inclusives, d’une période vide et de l’absence de filtre.
- Indicateur des stations les plus actives, classées par total de mouvements.
- Tests du classement, des comptages, des égalités et de la limite par défaut.
- Indicateur des incidents par statut et délai moyen de résolution.
- Test des comptages et du délai moyen sur les données importées.


## [0.0.3] - 2026-10-14

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
- Fiabilisation des trajets avec les fonctions testées.
- Conservation des trajets valides et journalisation des rejets.
- Journalisation des identifiants de vélo et horodatages normalisés.
- Fiabilisation des incidents et conservation des lignes valides.
- Journalisation des statuts normalisés, des rejets et des techniciens absents.
- Modèle ORM Station et chargement des stations avec SQLAlchemy.
- Vérification de deux chargements successifs : 120 stations, sans doublon.
- Modèle ORM Trajet et chargement des trajets avec SQLAlchemy.
- Vérification de deux chargements successifs : 2 002 trajets, sans doublon.
- Modèle ORM Incident et chargement des incidents avec SQLAlchemy.
- Vérification de deux chargements successifs des trois tables, sans doublon.
- Résultats des tests et mesure de couverture documentés dans le README.


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