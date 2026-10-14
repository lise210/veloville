from datetime import date

from api.database import SessionLocal
from api.services.indicateurs import activite_par_jour


def test_activite_par_jour_donnees_importees():
    with SessionLocal() as session:
        resultat = activite_par_jour(session, date(2026, 8, 24), date(2026, 8, 30))

    #calculer dans pgAdmin pour les 329, 311, ...
    assert resultat == {
        "donnees": [
            {"jour": "2026-08-24", "nb_trajets": 329},
            {"jour": "2026-08-25", "nb_trajets": 311},
            {"jour": "2026-08-26", "nb_trajets": 306},
            {"jour": "2026-08-27", "nb_trajets": 300},
            {"jour": "2026-08-28", "nb_trajets": 315},
            {"jour": "2026-08-29", "nb_trajets": 219},
            {"jour": "2026-08-30", "nb_trajets": 222}]}


def test_activite_par_jour_un_seul_jour():
    with SessionLocal() as session:
        resultat = activite_par_jour(
            session,
            date(2026, 8, 24),
            date(2026, 8, 24))

    assert resultat == {"donnees": [{"jour": "2026-08-24", "nb_trajets": 329}]}


def test_activite_par_jour_periode_vide():
    with SessionLocal() as session:
        resultat = activite_par_jour(
            session,
            date(2026, 1, 1),
            date(2026, 1, 2))

    assert resultat == {"donnees": []}


def test_activite_par_jour_sans_dates():
    with SessionLocal() as session:
        resultat = activite_par_jour(session)
    donnees = resultat["donnees"]

    assert len(donnees) == 7
    assert donnees[0]["jour"] == "2026-08-24"
    assert donnees[-1]["jour"] == "2026-08-30"
    assert sum(ligne["nb_trajets"] for ligne in donnees) == 2002