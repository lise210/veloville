"""Fixtures pytest communes.

À compléter : client TestClient de l'API, jetons pour exploitant01 et direction01,
session de base de données de test. Aucun secret en dur : lire .env.
"""

import pytest
from fastapi.testclient import TestClient
import os

from api.main import app

@pytest.fixture(scope="session")
def client():
    """Appelle FastAPI en mémoire : Uvicorn n'est pas nécessaire"""
    with TestClient(app) as test_client:
        yield test_client


def connexion_et_token(client, username):
    """Connecte un compte et récupère son JWT."""
    reponse = client.post("/auth/login",
        json={
            "username": username,
            "password": os.environ["TEST_PASSWORD"]})

    assert reponse.status_code == 200
    return reponse.json()["access_token"]

@pytest.fixture(scope="session")
def exploitant_token(client):
    return connexion_et_token(client, "exploitant01")

@pytest.fixture(scope="session")
def direction_token(client):
    return connexion_et_token(client, "direction01")