"""Fixtures pytest communes.

À compléter : client TestClient de l'API, jetons pour exploitant01 et direction01,
session de base de données de test. Aucun secret en dur : lire .env.
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app

@pytest.fixture(scope="session")
def client():
    """Appelle FastAPI en mémoire : Uvicorn n'est pas nécessaire"""
    with TestClient(app) as test_client:
        yield test_client

        