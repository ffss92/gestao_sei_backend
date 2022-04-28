from typing import Optional
from pydantic import BaseModel
from datetime import datetime
# from .team_assignment import TeamAssignment


class TeamCreate(BaseModel):
  name: str
  description: Optional[str] = None
  is_active: Optional[bool] = None

class TeamUpdate(TeamCreate):
  name: Optional[str] = None

class TeamDB(TeamCreate):
  id: int
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode = True

class Team(TeamDB):
  pass