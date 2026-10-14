"""Modèles ORM SQLAlchemy : Station, Trajet, Incident, Utilisateur.

À compléter : déclarer les quatre tables conformément à sql/schema.sql.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy import String, Integer, Numeric, Date
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