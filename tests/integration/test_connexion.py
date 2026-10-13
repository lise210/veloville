"""Test de connexion à PostgreSQL"""

from sqlalchemy import text

from api.database import engine

def test_connexion_postgresql():
    with engine.connect() as connexion:
        resultat = connexion.execute(text("SELECT current_database(), current_user")).one()
        #one() : récupère une ligne de résultat. resultat = ("veloville", "veloville")

    assert resultat[0] == "veloville"
    assert resultat[1] == "veloville"