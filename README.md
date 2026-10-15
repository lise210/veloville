# VéloVille — Projet Bloc 2 : Plateforme de valorisation des données

Application de valorisation des données de VéloVille :
fiabilisation des exports CSV, API sécurisée et restitution avec Streamlit.

Le développement suit le cahier des charges de référence fourni avec le sujet

## État actuel

La préparation de l’environnement est réalisée :

- dépendances installées et versions enregistrées,
- configuration locale dans `.env`, 
- script de génération du secret JWT 
- rôle et base PostgreSQL `veloville` créés, 
- connexion SQLAlchemy configurée, 
- test de connexion PostgreSQL réussi.
- Tables station, trajet, incident et utilisateur créées avec leurs contraintes.
- Index créés pour les filtres et les indicateurs.
- Script sql/schema.sql exécuté deux fois sans erreur --> rejouable.
- Comptes exploitant01 et direction01 chargés avec leurs rôles.
- Droits de lecture, insertion et modification vérifiés pour le rôle PostgreSQL veloville sur les quatre tables.
- Audit des trois CSV réalisé avec Python et Pandas.
- Fonctions de fiabilisation vérifiées par des tests unitaires.
- Modèles ORM Station, Trajet et Incident définis.
- Import réalisé : 120 stations, 2 002 trajets et 177 incidents.
- Deux exécutions successives sans doublon supplémentaire.
- Journal des doublons, rejets, normalisations et avertissements créé.

Les trois indicateurs sont développés et vérifiés par des tests d’intégration :
activité par jour, classement des stations actives et incidents par statut avec délai moyen de résolution.

Les routes API, l’authentification JWT, les contrôles de rôles et l’interface Streamlit sont développés. 
Les vérifications manuelles des contraintes SQL sont documentées dans docs/schema-donnees.md.

## Technologies et prérequis

- Windows et PowerShell pour les commandes ci-dessous,
- Python 3.14.7 utilisé pendant le développement,
- PostgreSQL 18 utilisé pendant le développement, avec pgAdmin,
- Git,
- FastAPI, SQLAlchemy, Psycopg, Streamlit et pytest.

Le sujet prévoit Python 3.12. Le développement est actuellement effectué avec Python 3.14.7. L’installation des dépendances et le test de connexion ont été vérifiés avec cette version. 

Les versions des bibliothèques sont fixées dans `requirements.txt`.

## Récupérer le projet

Le dépôt GitHub est privé : un accès est nécessaire (il sera repassé en public avant l'envoie!).

Cloner le projet et sélectionner la branche de travail actuelle :

```powershell
git clone https://github.com/lise210/veloville.git
cd veloville
```

La branche main contient les étapes déjà validées.

Les commandes suivantes sont exécutées depuis le dossier veloville.

## Préparer l’environnement Python

Créer puis activer l’environnement virtuel :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
python -m pip install -r requirements.txt
```

Le dossier `.venv` est exclu de Git. Sur un autre ordinateur, il doit être recréé.

## Configurer les variables d’environnement

Si `.env` n’existe pas encore, le créer depuis le modèle :

```powershell
Copy-Item .env.example .env
```

Variables attendues :

| Variable | Utilité |
|---|---|
| `DATABASE_URL` | Connexion à PostgreSQL |
| `JWT_SECRET` | Secret de signature des jetons JWT |
| `JWT_ALGORITHM` | Algorithme de signature, `HS256` |
| `JWT_EXPIRATION_MINUTES` | Durée de validité des jetons |
| `API_URL` | Adresse de l’API utilisée par Streamlit |
| `API_TIMEOUT_SECONDES` | Délai maximal des appels HTTP |
| `TEST_PASSWORD` | Mot de passe des comptes de recette utilisé par les tests |

Pour exécuter les tests de connexion, renseigner TEST_PASSWORD dans .env avec le mot de passe des comptes de recette fourni dans l’énoncé.

Générer le secret JWT :

```powershell
python scripts/generate_jwt_secret.py
```

Copier la valeur obtenue après `JWT_SECRET=` dans `.env`.

Pour la configuration locale fournie :

```dotenv
DATABASE_URL=postgresql+psycopg://veloville:veloville@localhost:5432/veloville
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
API_URL=http://localhost:8000
API_TIMEOUT_SECONDES=5
```

Le secret JWT reste uniquement dans `.env`.
Ce fichier est exclu de Git.

## Préparer PostgreSQL avec pgAdmin

Se connecter au serveur PostgreSQL avec un compte administrateur.

### Créer le rôle

Dans `Login/Group Roles` --> `Create` --> `Login/Group Role` :

- nom : `veloville`,
- mot de passe local : `veloville`,
- activer `Can login?`.

### Créer la base

Dans `Databases` --> `Create` --> `Database` :

- nom : `veloville` ;
- propriétaire : `veloville`.

### Créer les tables et charger les comptes

Dans pgAdmin, ouvrir le Query Tool sur la base veloville
avec le rôle veloville.

1. Ouvrir et exécuter sql/schema.sql.
2. Relancer le script : les tables et index existants sont conservés.
3. Ouvrir et exécuter sql/comptes.sql.

Vérifier les comptes :

```sql
SELECT id_utilisateur, username, role
FROM utilisateur
ORDER BY id_utilisateur;
```

Résultat attendu :

|username|role|
|---|---|
|exploitant01|exploitant|
|direction01|direction|


La réexécution de schema.sql conserve les tables et les données grâce à IF NOT EXISTS. Elle ne met pas à jour la structure d’une table déjà existante.

## Importer les données

Depuis la racine du projet, avec l’environnement virtuel activé :

```powershell
python -m scripts.importer
```

Le script :

- lit les trois CSV avec Pandas 
- applique les fonctions de fiabilisation 
- écarte les doublons et les lignes invalides 
- écrit le journal dans `docs/journal_import.csv` 
- charge les stations, puis les trajets et les incidents avec SQLAlchemy.

Les lignes dont l’identifiant existe déjà en base ne sont pas réinsérées
ni remplacées. Deux exécutions successives ont conservé les mêmes volumes :

| Table | Nombre de lignes |
|---|---:|
| station | 120 |
| trajet | 2 002 |
| incident | 177 |

Le journal est remplacé à chaque exécution.
Il contient 192 messages sur les données fournies :
12 doublons, 19 rejets, 136 normalisations et 25 avertissements.

Un message de normalisation ou d’avertissement ne signifie pas
que la ligne est rejetée.

## Lancer l’API et l’interface

Depuis la racine du projet, avec l’environnement virtuel activé, ouvrir deux terminaux.

Dans le premier, démarrer l’API :

```powershell
python -m uvicorn api.main:app --reload
```

Dans le second, démarrer Streamlit :

```powershell
python -m streamlit run front/app.py
```

Ouvrir http://localhost:8501, puis se connecter avec un compte de recette (donné dans l'énoncé).

Le menu latéral donne accès aux stations, aux incidents et aux indicateurs.
Les deux rôles peuvent consulter les données. Seul le rôle exploitant dispose du formulaire de changement de statut des incidents.

Pour arrêter chaque serveur, utiliser Ctrl+C dans son terminal.

## Vérifier la connexion PostgreSQL

Le test utilise la configuration de `.env` et vérifie que
la connexion concerne la base et le compte `veloville`.
Il ne modifie aucune donnée.

```powershell
python -m pytest tests/integration/test_connexion.py -v
```

Résultat obtenu pendant la préparation :

```text
1 passed
```

Ce résultat concerne uniquement le test de connexion.


## Tester les fonctions de fiabilisation

```powershell
python -m pytest tests/unit/test_fiabilisation.py -v
```

Dernier résultat obtenu : 134 passed.
Ces tests vérifient les fonctions sans accéder à PostgreSQL.

## Tests et couverture des modules métier

Depuis la racine du projet, avec l’environnement virtuel activé :

```powershell
pytest --cov=api/services --cov-report=term-missing
```

Cette commande exécute les tests et mesure la couverture. Le rapport indique également les lignes non exécutées.

Résultat obtenu le 15/10/2026 :

- 173 tests réussis : 134 tests unitaires de fiabilisation, 3 tests unitaires des réponses des indicateurs, 1 test de connexion, 7 tests d’intégration des indicateurs et 28 tests d’API.
- Couverture globale de api/services : 95 %, supérieure au minimum demandé de 60 %.
- 260 instructions mesurées, dont 12 non exécutées dans le service incidents.
- Changement de statut vérifié manuellement depuis Streamlit sur un incident temporaire : `ouvert` --> `en_cours` --> `resolu`, avec date de résolution automatique.

La couverture indique les instructions exécutées pendant les tests.

## Organisation du projet

```text
api/
  config.py            Chargement de la configuration
  database.py          Connexion et sessions SQLAlchemy
  models.py            Modèles Station, Trajet, Incident et Utilisateur
  schemas.py           Schémas de validation des entrées et sorties
  securite.py          Authentification JWT et contrôle des rôles
  routers/             Routes API
  services/            Fiabilisation, consultations et indicateurs

data/                  Exports CSV fournis
docs/                  Documentation et recette
front/                 Interface Streamlit
scripts/               Génération du secret, import et sauvegarde
sql/                   Schéma et comptes PostgreSQL
tests/
  unit/                Tests des fonctions de fiabilisation
  integration/         Tests d’intégration
```

## Gestion de Git et GitHub

- `main` rassemble les étapes validées.
- Une branche dédiée est utilisée pour chaque tâche.
- Les modifications sont enregistrées dans des commits explicites.
- Les commits sont envoyés régulièrement sur GitHub.
- Une pull request permet d’examiner les changements avant leur fusion.
- Les versions identifiées dans le changelog sont associées à des tags.


configuration/environnement : préparation terminée et fusionnée dans main par la pull request n°1.

fonctionnalite/schema-donnees : schéma et audit terminés, fusionnés dans main par la pull request n°2.

fonctionnalite/import-donnees : fiabilisation et chargement des CSV terminés, fusionnés dans main par la pull request n°3.

fonctionnalite/indicateurs : trois indicateurs développés et fusionnés dans main.

Le tag `v0.0.0` identifie le squelette initial fourni, au commit `123bdcb`.

Le tag `v0.0.1` identifie l’environnement configuré et la connexion PostgreSQL vérifiée, au commit de fusion 5f63809.

Le tag `v0.0.2` identifie le schéma et l’audit des trois CSV.

Le tag `v0.0.3` identifie la fiabilisation et l’import des données.

Le tag `v0.0.4` identifie les trois indicateurs.

Le tag `v0.0.5` identifie l’API sécurisée.

Le tag `v0.0.6` identifie l’interface Streamlit.

Les fichiers `.env`, les environnements virtuels et les sauvegardes
sont exclus du dépôt.

## Choix écoresponsables

### Pagination côté serveur

Les listes sont paginées dans PostgreSQL avec offset et limit. L’API renvoie 20 résultats par défaut et accepte au maximum 100 résultats par page, afin de limiter les données transférées et affichées.

### Chargement à la demande

L’interface ne comporte aucun rafraîchissement automatique. Les filtres sont regroupés dans des formulaires : les changements sont appliqués après validation par l’utilisateur.

### Mise en cache des communes

La liste des communes des stations est conservée en cache pendant une heure avec st.cache_data. Cela évite de relire le référentiel à chaque affichage.

### Agrégations dans PostgreSQL

Les indicateurs sont calculés avec des agrégations SQL. L’interface reçoit les résultats des calculs sans charger tous les trajets ou incidents pour les recalculer en Python.

### Restitution tabulaire

L’interface utilise des tableaux et des valeurs clés, conformément au périmètre demandé, sans bibliothèque de graphiques supplémentaire.

## Difficultés rencontrées et solutions

### Git non reconnu dans le terminal VS Code

Git était installé, mais son dossier n’était pas accessible dans le terminal VS Code.

Correction temporaire appliquée au terminal (obligé de lancer cette commande à chaque nouveau terminal) :

```powershell
$env:Path = "C:\Program Files\Git\cmd;$env:Path"
```

### Chemin trop long pendant l’installation

L’installation de Streamlit a échoué avec `WinError 206` dans le dossier initial, dont le chemin était très long.

Le projet a été copié dans un emplacement plus court (Documents en local), en conservant `.git`. L’environnement `.venv` a été recréé,
puis l’installation a réussi.

### Encodage de requirements.txt

La commande `pip freeze > requirements.txt` a produit un fichier en UTF-16.

Le fichier a été enregistré en UTF-8 avec VS Code, puis la correction a été commitée.

### Tables créées avec le compte postgres

Les tables ont initialement été créées avec le compte administrateur
`postgres`. Le rôle applicatif `veloville` ne disposait donc pas des
droits nécessaires sur ces tables.

Leur propriété a été transférée avec les commandes suivantes,
exécutées avec le compte administrateur :

```sql
ALTER TABLE public.station OWNER TO veloville;
ALTER TABLE public.trajet OWNER TO veloville;
ALTER TABLE public.incident OWNER TO veloville;
ALTER TABLE public.utilisateur OWNER TO veloville;
```

Les droits `SELECT`, `INSERT` et `UPDATE` ont ensuite été vérifiés
avec `has_table_privilege` : ils sont accordés sur les quatre tables.

Pour une nouvelle installation, exécuter directement `schema.sql` avec le rôle `veloville`.

### Incident modifié pendant les essais manuels

Un incident importé (I2026-0065) a été passé au statut resolu pendant les essais de l’interface. Trois tests ont alors échoué, car les comptages par statut et le délai moyen ne correspondaient plus aux données initiales.

La ligne a été comparée au CSV source, puis restaurée en base : statut ouvert et date de résolution à NULL.

Après correction, les 170 tests réussissent à nouveau, avec 95 % de couverture des services.

Pour les prochains essais de modification, utiliser un incident temporaire, vérifier son identifiant avant validation, puis le supprimer après l’essai.

## Recette fonctionnelle

Le relevé initial comporte 8 cas OK et 2 cas KO.
Les deux anomalies de messages HTTP ont été corrigées et les cas REC-06 et REC-08 rejoués avec succès.

Les résultats consolidés sont de 10 cas OK.
Les résultats détaillés, les limites de traçabilité et le procès-verbal se trouvent dans `docs/recette/resultats-recette.md`

## Étapes restantes

- sauvegarde et restauration,
- tests unitaires des indicateurs,
- procédure de déploiement,
- finalisation de la documentation et livraison.

## Auteur

Lise