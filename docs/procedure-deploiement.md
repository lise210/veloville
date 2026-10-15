# Procédure de déploiement

Cette procédure décrit l’installation locale de VéloVille sous Windows.
Les commandes PowerShell sont exécutées depuis la racine du projet,
dans le dossier contenant requirements.txt.

## 1. Prérequis

Environnement utilisé et vérifié pendant le développement :

- Windows,
- Python 3.14.7,
- PostgreSQL 18 avec pgAdmin,
- Git.

Le sujet prévoit Python 3.12 et PostgreSQL 14 ou supérieur.
La compatibilité avec Python 3.12 n’a pas été vérifiée.

## 2. Récupérer le projet

Le dépôt GitHub est public et peut être cloné sans accès particulier.

```powershell
git clone https://github.com/lise210/veloville.git
cd veloville
```

Le clonage sélectionne la branche main.

## 3. Préparer l’environnement Python

Créer et activer l’environnement virtuel :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
python -m pip install -r requirements.txt
```

L’environnement virtuel doit être activé dans chaque terminal utilisé
pour lancer les commandes Python.

## 4. Configurer les variables d’environnement

Créer le fichier local de configuration :

```powershell
Copy-Item .env.example .env
```

Renseigner les variables suivantes :

| Variable | Valeur ou rôle |
|---|---|
| `DATABASE_URL` | Connexion à PostgreSQL |
| `JWT_SECRET` | Secret de signature à générer |
| `JWT_ALGORITHM` | HS256 |
| `JWT_EXPIRATION_MINUTES` | 60 |
| `API_URL` | http://localhost:8000 |
| `API_TIMEOUT_SECONDES` | 5 |
| `TEST_PASSWORD` | Mot de passe des comptes de recette fourni dans l’énoncé |

Générer le secret JWT :

```powershell
python scripts/generate_jwt_secret.py
```

Copier la valeur générée après "JWT_SECRET=" dans .env.

Le fichier .env reste local et ne doit pas être envoyé sur GitHub.

## 5. Préparer PostgreSQL

### Créer le rôle

Dans pgAdmin, se connecter au serveur avec le compte administrateur postgres.

Dans Login/Group Roles --> Create --> Login/Group Role :

- nom : veloville,
- mot de passe local : veloville,
- onglet Privileges : activer Can login?


### Créer la base

Dans Databases --> Create --> Database :

- nom : veloville,
- propriétaire : veloville.

### Créer les tables et charger les comptes

Ouvrir le Query Tool sur la base veloville avec le rôle veloville.
Vérifier la connexion :

```sql
SELECT current_database(), current_user;
```

Les deux valeurs doivent être veloville.

Exécuter le contenu de sql/schema.sql, puis celui de sql/comptes.sql.

Vérifier les comptes :

```sql
SELECT username, role
FROM utilisateur
ORDER BY username;
```

Résultat attendu :
- direction01 : direction ;
- exploitant01 : exploitant.

### Vérifier DATABASE_URL

Dans .env, utiliser pour cette configuration locale :

```dotenv
DATABASE_URL=postgresql+psycopg://veloville:veloville@localhost:5432/veloville
```

Si le port, le compte ou le mot de passe diffèrent, adapter cette valeur.

## 6. Importer les données

Depuis la racine du projet, avec .venv activé :

```powershell
python -m scripts.importer
```

Résultat attendu :

| Table | Nombre de lignes |
|---|---:|
| station | 120 |
| trajet | 2 002 |
| incident | 177 |

Le journal est écrit dans docs/journal_import.csv.
Il contient les doublons, rejets, normalisations et avertissements.

Une nouvelle exécution ne réinsère pas les identifiants déjà présents.

## 7. Lancer l’API

Dans un premier terminal, avec .venv activé :

```powershell
python -m uvicorn api.main:app --reload
```

Laisser le terminal ouvert.

Documentation interactive : http://127.0.0.1:8000/docs

## 8. Lancer l’interface Streamlit

Dans un second terminal, depuis la racine du projet :

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run front/app.py
```

Ouvrir http://localhost:8501.

Se connecter avec exploitant01 ou direction01 et le mot de passe
des comptes de recette fourni dans l’énoncé.

Pour arrêter les serveurs, utiliser Ctrl+C dans chacun des terminaux.

## 9. Vérifications après déploiement

- GET /sante renvoie 200 avec {"statut": "ok"}.
- La connexion fonctionne avec les deux comptes.
- Les stations, incidents et indicateurs sont consultables.
- Le formulaire de changement de statut est visible uniquement pour l’exploitant.

Sur la base contenant les données initiales importées, exécuter :

```powershell
python -m pytest --cov=api/services --cov-report=term-missing
```

Résultat de référence : 173 tests réussis et 95 % de couverture des services.

Les tests d’intégration utilisent PostgreSQL. Les tests de comptage attendent
les données initiales : toute modification manuelle doit être annulée
avant leur exécution.

## 10. Sauvegarde et restauration — non réalisées

Le script de sauvegarde demandé n’est pas complété.
La sauvegarde et la restauration n’ont pas été vérifiées.
N'a pas été vu en formation, cette partie reste à réaliser avant l'oral final (je me renseignerai sur le sujet).