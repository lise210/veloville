"""Chargement de la configuration du backend"""

import os
from dotenv import load_dotenv

# charge les variables du fichier .env
load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]