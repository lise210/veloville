"""Routeur auth.

À compléter : POST /auth/login.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Utilisateur
from api.schemas import LoginRequest, TokenResponse
from api.securite import creer_token, verifier_mot_de_passe


router = APIRouter(prefix="/auth", tags=["Authentification"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Vérifie les identifiants puis délivre un JWT"""
    utilisateur = db.scalar(select(Utilisateur).where(Utilisateur.username == data.username))
    if utilisateur is None or not verifier_mot_de_passe(data.password, utilisateur.mot_de_passe_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Identifiants invalides")

    token = creer_token(username=utilisateur.username, role=utilisateur.role)

    return TokenResponse(access_token=token, role=utilisateur.role)