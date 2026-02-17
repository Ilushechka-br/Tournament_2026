from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "team"

class TournamentShort(BaseModel):
    id: int
    title: str
    status: str
    class Config:
        from_attributes = True

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

class RoundCreate(BaseModel):
    title: str
    description: str
    requirements: str 
    start_time: datetime
    end_time: datetime
    tournament_id: int
    
class RoundOut(RoundCreate):
    id: int
    status: str = "Draft"
    class Config:
        from_attributes = True

class LeaderboardEntry(BaseModel):
    team_name: str
    total_score: float
    tech_avg: float
    func_avg: float
    submissions_count: int

    class Config:
        from_attributes = True
        