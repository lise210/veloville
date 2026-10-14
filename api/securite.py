"""Authentification et autorisation.

À compléter : vérification d'un mot de passe contre son hachage bcrypt, création et
décodage du JWT (secret et algorithme lus dans l'environnement),
dépendances utilisateur_courant() et exiger_role("exploitant").
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from api.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_MINUTES

#comme dependencies.py des exos
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import Utilisateur

#récupère le jeton envoyé dans l'en-tête
bearer_scheme = HTTPBearer(auto_error=False)

def verifier_mot_de_passe(mot_de_passe: str, mot_de_passe_hash: str) -> bool:
    """Compare le mot de passe saisi avec le hachage stocké"""
    return bcrypt.checkpw(
        mot_de_passe.encode("utf-8"),
        mot_de_passe_hash.encode("utf-8"))

def creer_token(username: str, role: str) -> str:
    """Crée un JWT signé contenant l'identité et le rôle"""
    maintenant = datetime.now(timezone.utc)
    expiration = maintenant + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    contenu = {
        "sub": username,
        "role": role,
        "iat": maintenant,
        "exp": expiration}
    return jwt.encode(contenu, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decoder_token(token: str) -> dict:
    """Vérifie la signature et l'expiration du JWT"""
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

def utilisateur_courant(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Utilisateur:
    """Authentifie l'utilisateur à partir du JWT"""

    # Aucun token reçu
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise",
            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        #contient le JWT sans le mot "Bearer"
        contenu = decoder_token(credentials.credentials)
        # sub contient le nom de l'utilisateur
        username = contenu.get("sub")

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"})

    # Recherche l'utilisateur dans PostgreSQL
    utilisateur = db.scalar(select(Utilisateur).where(Utilisateur.username == username))

    if utilisateur is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur inconnu",
            headers={"WWW-Authenticate": "Bearer"})

    return utilisateur

def exiger_role(*roles_autorises: str):
    """Crée une dépendance limitée aux rôles autorisés"""
    def verifier_role(utilisateur: Utilisateur = Depends(utilisateur_courant)) -> Utilisateur:
        if utilisateur.role not in roles_autorises:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Rôle non autorisé pour cette action")
        return utilisateur
    return verifier_role