"""Chargement de la configuration du backend"""

import os
from dotenv import load_dotenv

# charge les variables du fichier .env
load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]
JWT_EXPIRATION_MINUTES = int(os.environ["JWT_EXPIRATION_MINUTES"])