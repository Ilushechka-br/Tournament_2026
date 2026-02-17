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

@app.post("/rounds/", tags=["Admin"])
def create_round(round_data: schemas.RoundCreate, db: Session = Depends(database.get_db)):
    return crud.create_round(db, round_data)

@app.post("/submissions/", tags=["Teams"])
def submit_work(sub: schemas.SubmissionCreate, db: Session = Depends(database.get_db)):
    return crud.create_submission(db, sub)

@app.post("/rounds/{round_id}/distribute", tags=["Admin"])
def distribute_works(round_id: int, db: Session = Depends(database.get_db)):
    return crud.distribute_submissions_to_jury(db, round_id)

@app.get("/tournaments/{tournament_id}/leaderboard", response_model=List[schemas.LeaderboardEntry], tags=["Public"])
def read_leaderboard(tournament_id: int, db: Session = Depends(database.get_db)):
    return crud.get_leaderboard(db, tournament_id=tournament_id)

@app.get("/users/me/team", tags=["User Profile"])
def get_my_team_info(user_id: int, db: Session = Depends(database.get_db)):
    # Команда, де поточний юзер є капітаном
    return db.query(models.Team).filter(models.Team.captain_id == user_id).first()

@app.get("/users/me/evaluations", tags=["User Profile"])
def get_jury_assignments(user_id: int, db: Session = Depends(database.get_db)):
    # Список робіт, які призначені цьому журі
    return db.query(models.Evaluation).filter(models.Evaluation.jury_id == user_id).all()