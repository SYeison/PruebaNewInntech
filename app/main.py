from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, candidates, voters, votes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Votaciones API",
    description="API RESTful para gestionar votantes, candidatos y votos.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(voters.router)
app.include_router(candidates.router)
app.include_router(votes.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "Sistema de Votaciones API"}
