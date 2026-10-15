"""Tests des fonctions de calcul des indicateurs.

À compléter : vérifier les agrégats sur un jeu de données connu.
"""

from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal

from api.services.indicateurs import activite_par_jour, stations_actives, incidents_par_statut




def test_activite_par_jour_avec_resultats(mocker):
    """Vérifie les dates et les comptages renvoyés."""
    jour1 = mocker.Mock(jour=date(2026, 8, 24), nb_trajets=3)
    jour2 = mocker.Mock(jour=date(2026, 8, 25), nb_trajets=2)

    faux_resultat = mocker.Mock()
    faux_resultat.all.return_value = [jour1, jour2]

    mocker.patch("sqlalchemy.orm.Session.execute", return_value=faux_resultat)

    with Session() as session:
        resultat = activite_par_jour(session)

    assert resultat == {
        "donnees": [
            {"jour": "2026-08-24", "nb_trajets": 3},
            {"jour": "2026-08-25", "nb_trajets": 2}]}



def test_stations_actives_avec_resultat(mocker):
    """Vérifie les informations renvoyées pour une station en particulier"""
    station = mocker.Mock(
        station_id="S001",
        nom="Lille - Gare",
        nb_departs=3,
        nb_arrivees=2)

    faux_resultat = mocker.Mock()
    faux_resultat.all.return_value = [station]

    mocker.patch("sqlalchemy.orm.Session.execute", return_value=faux_resultat)

    with Session() as session:
        resultat = stations_actives(session)

    assert resultat == {
        "donnees": [
            {
                "station_id": "S001",
                "nom": "Lille - Gare",
                "nb_departs": 3,
                "nb_arrivees": 2}]}


def test_incidents_par_statut_avec_resultat(mocker):
    """Vérifie les comptages transmis et la conversion du délai"""
    ligne = mocker.Mock(statut="resolu", nb_incidents=2)
    faux_resultat = mocker.Mock()
    faux_resultat.all.return_value = [ligne]

    mocker.patch("sqlalchemy.orm.Session.execute", return_value=faux_resultat)
    mocker.patch("sqlalchemy.orm.Session.scalar", return_value=Decimal("12.5"))

    with Session() as session:
        resultat = incidents_par_statut(session)

    assert resultat == {
        "donnees": [
            {"statut": "resolu", "nb_incidents": 2}],
        "delai_moyen_resolution_heures": 12.5}
    assert isinstance(resultat["delai_moyen_resolution_heures"], float)

