from sqlalchemy.orm import Session
from . import models, schemas

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

def create_tournament(db: Session, tournament: schemas.TournamentCreate, user_id: int):
    db_tournament = models.Tournament(
        title=tournament.title,
        description=tournament.description,
        creator_id=user_id
    )
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

def get_user_tournaments(db: Session, user_id: int):
    return db.query(models.Tournament).filter(models.Tournament.creator_id == user_id).all()