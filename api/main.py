"""Point d'entrée de l'API VéloVille (FastAPI).

À compléter : créer l'application, inclure les routeurs (auth, stations, trajets,
incidents, indicateurs) et exposer GET /sante -> {"statut": "ok"}.

Lancement : uvicorn api.main:app --reload
"""

from fastapi import FastAPI

from api.routers import auth, stations

app = FastAPI(title="API VéloVille")

app.include_router(auth.router)
app.include_router(stations.router)

@app.get("/sante")
def sante():
    return {"statut": "ok"}