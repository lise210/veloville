# VéloVille — Plateforme de valorisation des données

À compléter : présentation du projet, prérequis, installation, lancement de
l'API et du front, exécution des tests, liens vers la documentation
(docs/), auteur et version.


# VéloVille — Projet Bloc 2

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

Les tables, l’import des données, les routes API, l’authentification et l’interface restent à développer.

## Technologies et prérequis

- Windows et PowerShell pour les commandes ci-dessous,
- Python 3.14.7 utilisé pendant le développement,
- PostgreSQL 14 ou supérieur, avec pgAdmin,
- Git,
- FastAPI, SQLAlchemy, Psycopg, Streamlit et pytest.

Le sujet prévoit Python 3.12. Le développement est actuellement effectué avec Python 3.14.7. L’installation des dépendances et le test de connexion ont été vérifiés avec cette version. 

Les versions des bibliothèques sont fixées dans `requirements.txt`.

## Récupérer le projet

Le dépôt GitHub est privé : un accès est nécessaire.

```powershell
git clone https://github.com/lise210/veloville.git
cd veloville
```

Pendant la préparation de l’environnement, les changements se trouvent
sur la branche suivante, avant leur fusion dans `main` :

```powershell
git switch configuration/environnement
```

Toutes les commandes suivantes sont exécutées depuis la racine
du projet, dans le dossier contenant `requirements.txt`.

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

Le dossier `.venv` est exclu de Git. Sur un autre ordinateur,
il doit être recréé.

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

La création des tables avec `sql/schema.sql` et le chargement des comptes avec `sql/comptes.sql` seront documentés lors de leur mise en place.

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
La suite complète de tests reste à développer.

## Organisation du projet

```text
api/
  config.py            Chargement de la configuration
  database.py          Connexion et sessions SQLAlchemy
  models.py            Modèles des tables à développer
  schemas.py           Schémas de validation à développer
  securite.py          Sécurité à développer
  routers/             Routes API à développer
  services/            Traitements métier à développer

data/                  Exports CSV fournis
docs/                  Documentation et recette
front/                 Interface Streamlit à développer
scripts/               Génération du secret, import et sauvegarde
sql/                   Schéma et comptes PostgreSQL
tests/
  unit/                Tests métier à développer
  integration/         Tests d’intégration
```

## Gestion de Git et GitHub

- `main` rassemble les étapes validées.
- Une branche dédiée est utilisée pour chaque tâche.
- Les modifications sont enregistrées dans des commits explicites.
- Les commits sont envoyés régulièrement sur GitHub.
- Une pull request permet d’examiner les changements avant leur fusion.
- Les versions identifiées dans le changelog sont associées à des tags.

Branche de préparation : `configuration/environnement`.

Le tag `v0.0.0` identifie le squelette initial fourni,
au commit `123bdcb`.

Les fichiers `.env`, les environnements virtuels et les sauvegardes
sont exclus du dépôt.

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

## Étapes restantes

- audit des fichiers CSV ;
- création du schéma SQL et chargement des comptes ;
- fiabilisation et import idempotent ;
- calcul des indicateurs ;
- API REST, authentification JWT et contrôle des rôles ;
- interface Streamlit tabulaire ;
- tests métier, couverture et recette ;
- sauvegarde et restauration ;
- finalisation de la documentation et livraison.

Les instructions de lancement de l’API et du front seront ajoutées
après leur implémentation.

## Auteur

Lise