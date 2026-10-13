"""Connexion à PostgreSQL (SQLAlchemy 2).

À compléter : lire DATABASE_URL depuis l'environnement (.env), créer l'engine, la
fabrique de sessions et la dépendance get_db() utilisée par les routeurs.
"""

"""Connexion PostgreSQL avec SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from api.config import DATABASE_URL

#configure l'accès à PostgreSQL
engine = create_engine(DATABASE_URL, pool_pre_ping=True,)

#crée les sessions pour lire/modifier les données
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase):
    """Classe de base commune aux modèles SQLAlchemy"""
    pass

def get_db():
    """Fournit une session puis la ferme après utilisation"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
