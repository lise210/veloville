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


def test_station_sans_token(client):
    """Vérifie qu'une station n'est pas accessible sans connexion"""
    reponse = client.get("/stations/S010")

    assert reponse.status_code == 401
    assert reponse.json() == {"detail": "Authentification requise"}


def test_station_avec_token_exploitant(client, exploitant_token):
    """Vérifie qu'un exploitant connecté peut consulter une station"""
    reponse = client.get("/stations/S010",
        headers={"Authorization": f"Bearer {exploitant_token}"})

    assert reponse.status_code == 200
    assert reponse.json()["station_id"] == "S010"


def test_station_avec_token_direction(client, direction_token):
    """Vérifie que la direction peut consulter une station"""
    reponse = client.get("/stations/S010",
        headers={"Authorization": f"Bearer {direction_token}"})

    assert reponse.status_code == 200
    assert reponse.json()["station_id"] == "S010"


def test_station_token_invalide(client):
    """Vérifie qu'un jeton invalide est refusé"""
    reponse = client.get("/stations/S010",
        headers={"Authorization": "Bearer token-invalide"})

    assert reponse.status_code == 401
    assert reponse.json() == {"detail": "Token invalide"}


def test_stations_pagination_par_defaut(client, exploitant_token):
    """Vérifie la première page des stations"""
    reponse = client.get("/stations",
        headers={"Authorization": f"Bearer {exploitant_token}"})

    assert reponse.status_code == 200
    contenu = reponse.json()
    assert contenu["total"] == 120
    assert contenu["page"] == 1
    assert contenu["taille_page"] == 20
    assert len(contenu["resultats"]) == 20
    assert contenu["resultats"][0]["station_id"] == "S001"


def test_stations_deuxieme_page(client, exploitant_token):
    """Vérifie le passage à la deuxième page."""
    reponse = client.get("/stations",
        params={"page": 2, "taille_page": 20},
        headers={"Authorization": f"Bearer {exploitant_token}"})

    assert reponse.status_code == 200
    contenu = reponse.json()
    assert contenu["total"] == 120
    assert contenu["page"] == 2
    assert contenu["taille_page"] == 20
    assert len(contenu["resultats"]) == 20
    assert contenu["resultats"][0]["station_id"] == "S021"


def test_stations_filtre_commune(client, exploitant_token):
    """Vérifie que seules les stations de Lille sont renvoyées"""
    reponse = client.get("/stations",
        params={"commune": "Lille", "taille_page": 100},
        headers={"Authorization": f"Bearer {exploitant_token}"})

    assert reponse.status_code == 200
    contenu = reponse.json()
    assert contenu["total"] > 0
    assert len(contenu["resultats"]) == contenu["total"]
    for station in contenu["resultats"]:
        assert station["commune"] == "Lille"


def test_stations_page_invalide(client, exploitant_token):
    """Vérifie qu'une page inférieure à 1 est refusée."""
    reponse = client.get("/stations",
        params={"page": 0},
        headers={"Authorization": f"Bearer {exploitant_token}"})

    assert reponse.status_code == 422


def test_stations_taille_page_trop_grande(client, exploitant_token):
    """Vérifie qu'une taille de page supérieure à 100 est refusé."""
    reponse = client.get("/stations",
        params={"taille_page": 101},
        headers={"Authorization": f"Bearer {exploitant_token}"})

    assert reponse.status_code == 422


def test_stations_taille_page_nulle(client, exploitant_token):
    """Vérifie qu'une taille de page égale à zéro est refusée"""
    reponse = client.get("/stations",
        params={"taille_page": 0},
        headers={"Authorization": f"Bearer {exploitant_token}"})

    assert reponse.status_code == 422


def test_trajets_pagination_par_defaut(client, exploitant_token):
    """Vérifie la première page des trajets"""
    reponse = client.get("/trajets",
        headers={"Authorization": f"Bearer {exploitant_token}"})

    assert reponse.status_code == 200
    contenu = reponse.json()
    assert contenu["total"] == 2002
    assert contenu["page"] == 1
    assert contenu["taille_page"] == 20
    assert len(contenu["resultats"]) == 20

    dates = [trajet["depart_horodatage"] for trajet in contenu["resultats"]]
    assert dates == sorted(dates)


def test_trajets_filtre_dates(client, exploitant_token):
    """Vérifie le filtre sur la journée du 24 août 2026."""
    reponse = client.get("/trajets",
        params={
            "date_debut": "2026-08-24",
            "date_fin": "2026-08-24"},
        headers={"Authorization": f"Bearer {exploitant_token}"})

    assert reponse.status_code == 200
    contenu = reponse.json()
    assert contenu["total"] == 329
    assert len(contenu["resultats"]) == 20
    for trajet in contenu["resultats"]:
        assert trajet["depart_horodatage"][:10] == "2026-08-24"


def test_trajets_filtre_station(client, exploitant_token):
    """Vérifie que la station est celle du départ ou de l'arrivée"""
    reponse = client.get("/trajets",
        params={"station": "S010", "taille_page": 100},
        headers={"Authorization": f"Bearer {exploitant_token}"})

    assert reponse.status_code == 200
    contenu = reponse.json()
    assert contenu["total"] > 0
    assert len(contenu["resultats"]) > 0
    for trajet in contenu["resultats"]:
        assert (trajet["station_depart"] == "S010" or trajet["station_arrivee"] == "S010")


def test_trajets_sans_token(client):
    """Vérifie que les trajets ne sont pas accessibles sans connexion"""
    reponse = client.get("/trajets")

    assert reponse.status_code == 401
    assert reponse.json() == {"detail": "Authentification requise"}


def test_incidents_pagination_par_defaut(client, exploitant_token):
    """Vérifie la première page et le tri des incidents"""
    reponse = client.get("/incidents",
        headers={"Authorization": f"Bearer {exploitant_token}"})

    assert reponse.status_code == 200
    contenu = reponse.json()
    assert contenu["total"] == 177
    assert contenu["page"] == 1
    assert contenu["taille_page"] == 20
    assert len(contenu["resultats"]) == 20
    dates = [incident["date_signalement"] for incident in contenu["resultats"]]
    assert dates == sorted(dates, reverse=True)


def test_incidents_filtre_statut(client, exploitant_token):
    """Vérifie le filtre sur les incidents ouverts."""
    reponse = client.get("/incidents",
        params={"statut": "ouvert", "taille_page": 100},
        headers={"Authorization": f"Bearer {exploitant_token}"})

    assert reponse.status_code == 200
    contenu = reponse.json()
    assert contenu["total"] == 55
    assert len(contenu["resultats"]) == 55
    for incident in contenu["resultats"]:
        assert incident["statut"] == "ouvert"


def test_incidents_sans_token(client):
    """Vérifie que la consultation exige une connexion"""
    reponse = client.get("/incidents")

    assert reponse.status_code == 401
    assert reponse.json() == {"detail": "Authentification requise"}