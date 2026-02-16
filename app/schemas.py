from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "team"

class UserOut(UserBase):
    id: int
    role: str
    tournaments: list[TournamentShort] = []

    class Config:
        from_attributes = True

class TournamentCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TournamentOut(BaseModel):
    id: int
    title: str
    status: str
    creator_id: int
    class Config:
        from_attributes = True

class TournamentShort(BaseModel):
    id: int
    title: str
    status: str
    class Config:
        from_attributes = True

