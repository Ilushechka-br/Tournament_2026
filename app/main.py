from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Tournament Platform API")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/tournaments/", response_model=schemas.TournamentOut, tags=["Admin"])
def create_tournament(tournament: schemas.TournamentCreate, db: Session = Depends(database.get_db)):
    return crud.create_tournament(db=db, tournament=tournament)

@app.post("/teams/", response_model=schemas.TeamOut, tags=["Teams"])
def register_new_team(team: schemas.TeamCreate, db: Session = Depends(database.get_db)):
    return crud.register_team(db=db, team_data=team)

@app.get("/")
def home():
    return {"status": "ok"}