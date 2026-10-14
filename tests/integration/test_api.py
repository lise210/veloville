"""Tests d'intégration de l'API avec TestClient.

À compléter : au moins /sante, /auth/login (OK et KO), une route protégée sans jeton
(401), PUT /incidents/{id}/statut avec le rôle direction (403).
"""

import os

def test_sante(client):
    """Vérifie que l'API répond correctement."""
    reponse = client.get("/sante")

    assert reponse.status_code == 200
    assert reponse.json() == {"statut": "ok"}


def test_login_exploitant(client):
    """Vérifie la connexion du compte exploitant"""
    reponse = client.post("/auth/login",
        json={
            "username": "exploitant01",
            "password": os.environ["TEST_PASSWORD"]})

    assert reponse.status_code == 200
    contenu = reponse.json()
    assert contenu["role"] == "exploitant"
    assert contenu["token_type"] == "bearer"
    assert contenu["access_token"]


def test_login_mauvais_mot_de_passe(client):
    """Vérifie qu'un mauvais mot de passe est refusé"""
    reponse = client.post("/auth/login",
        json={
            "username": "exploitant01",
            "password": "incorrect"})

    assert reponse.status_code == 401
    assert reponse.json() == {"detail": "Identifiants invalides"}


def test_login_utilisateur_inconnu(client):
    """Vérifie qu'un compte inexistant est refusé"""
    reponse = client.post("/auth/login",
        json={
            "username": "inconnu",
            "password": os.environ["TEST_PASSWORD"]})

    assert reponse.status_code == 401
    assert reponse.json() == {"detail": "Identifiants invalides"}


def test_login_direction(client):
    """Vérifie la connexion du compte direction"""
    reponse = client.post("/auth/login",
        json={
            "username": "direction01",
            "password": os.environ["TEST_PASSWORD"]})

    assert reponse.status_code == 200
    contenu = reponse.json()
    assert contenu["role"] == "direction"
    assert contenu["token_type"] == "bearer"
    assert contenu["access_token"]