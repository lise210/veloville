"""Modèles ORM SQLAlchemy : Station, Trajet, Incident, Utilisateur.

À compléter : déclarer les quatre tables conformément à sql/schema.sql.
"""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import String, Integer, Numeric, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from api.database import Base

class Station(Base):
    """Station"""
    __tablename__ = "station"
    station_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    commune: Mapped[str] = mapped_column(String(100))
    capacite: Mapped[int] = mapped_column(Integer)
    latitude: Mapped[Decimal] = mapped_column(Numeric(8, 5))
    longitude: Mapped[Decimal] = mapped_column(Numeric(8, 5))
    date_mise_en_service: Mapped[date] = mapped_column(Date)

class Trajet(Base):
    """Trajet"""
    __tablename__ = "trajet"
    trajet_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    velo_id: Mapped[str] = mapped_column(String(8))
    depart_horodatage: Mapped[datetime] = mapped_column(DateTime)
    station_depart: Mapped[str] = mapped_column(String(10), ForeignKey("station.station_id"))
    station_arrivee: Mapped[str | None] = mapped_column(String(10), ForeignKey("station.station_id"), nullable=True)
    duree_secondes: Mapped[int] = mapped_column(Integer)
    type_usager: Mapped[str] = mapped_column(String(20))
    usager_ref: Mapped[str | None] = mapped_column(String(9), nullable=True)

class Incident(Base):
    """Incident"""
    __tablename__ = "incident"
    incident_id: Mapped[str] = mapped_column(String(12), primary_key=True)
    date_signalement: Mapped[datetime] = mapped_column(DateTime)
    cible: Mapped[str] = mapped_column(String(20))
    velo_id: Mapped[str | None] = mapped_column(String(8), nullable=True)
    station_id: Mapped[str | None] = mapped_column(String(10), ForeignKey("station.station_id"), nullable=True)
    type_incident: Mapped[str] = mapped_column(String(100))
    statut: Mapped[str] = mapped_column(String(20))
    date_resolution: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    technicien: Mapped[str | None] = mapped_column(String(100), nullable=True)

class Utilisateur(Base):
    """Compte utilisateur de l'application"""
    __tablename__ = "utilisateur"
    id_utilisateur: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    mot_de_passe_hash: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(String(20))