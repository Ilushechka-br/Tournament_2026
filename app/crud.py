from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from fastapi import HTTPException

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        hashed_password=user.password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_tournament(db: Session, tournament: schemas.TournamentCreate):
    db_tournament = models.Tournament(
        title=tournament.title,
        description=tournament.description,
        reg_start=tournament.reg_start,
        reg_end=tournament.reg_end,
        status="draft" # Початковий статус
    )
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

def update_tournament_status(db: Session, tournament_id: int, status: str):
    db_tournament = db.query(models.Tournament).filter(models.Tournament.id == tournament_id).first()
    if db_tournament:
        db_tournament.status = status
        db.commit()
    return db_tournament

def get_user_tournaments(db: Session, user_id: int):
    return db.query(models.Tournament).filter(models.Tournament.creator_id == user_id).all()

def register_team(db: Session, team_data: schemas.TeamCreate):

    tournament = db.query(models.Tournament).filter(models.Tournament.id == team_data.tournament_id).first()
    
    if not tournament or tournament.status != "registration":
        raise HTTPException(status_code=400, detail="Реєстрація на цей турнір закрита або ще не почалася")


    now = datetime.utcnow()
    if not (tournament.reg_start <= now <= tournament.reg_end):
        raise HTTPException(status_code=400, detail="Ви поза межами реєстраційного вікна")


    db_team = models.Team(
        name=team_data.name,
        tournament_id=team_data.tournament_id,
        captain_email=team_data.captain_email
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    # Додавання учасників
    for member in team_data.members:
        db_member = models.TeamMember(
            full_name=member.full_name,
            email=member.email,
            team_id=db_team.id
        )
        db.add(db_member)
    
    db.commit()
    return db_team