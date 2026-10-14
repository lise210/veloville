# Journal des versions

Une section par version, avec les changements regroupés en
« Ajouté », « Modifié », « Corrigé ».

## [Non livré]

### Ajouté
- Fonction de normalisation des statuts d’incident (normaliser_statut).
- Tests unitaires des statuts valides, à normaliser, inconnus et absents.


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