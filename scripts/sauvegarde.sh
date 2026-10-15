#!/usr/bin/env bash

#arrête si une commande échoue
set -e

# se placer à la racine du projet
cd "$(dirname "$0")/.."

# Lire la connexion depuis .env
connexion=$(python -c "import os; from dotenv import load_dotenv; load_dotenv('.env'); print(os.environ['DATABASE_URL'], end='')")

# Adapter l'URL pour pg_dump
connexion="${connexion/postgresql+psycopg:/postgresql:}"

# créer le dossier 
mkdir -p sauvegardes
fichier="sauvegardes/veloville_$(date +%Y%m%d_%H%M%S).dump"

# sauvegarder : -Fc correspond au format custom
pg_dump --no-password -Fc --file="$fichier" --dbname="$connexion"

echo "Sauvegarde créée : $fichier"

