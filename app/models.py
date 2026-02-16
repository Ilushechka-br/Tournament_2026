import enum
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    ORGANIZER = "organizer"
    TEAM = "team"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default=UserRole.TEAM)
    tournaments = relationship("Tournament", back_populates="creator")

class Tournament(Base):
    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="open")
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="tournaments")