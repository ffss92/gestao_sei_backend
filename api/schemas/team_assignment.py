from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TeamAssignmentCreate(BaseModel):
  description: str
  team_id: int

class TeamAssignmentUpdate(BaseModel):
  description: Optional[str] = None
  # team_id: Optional[int] = None

class TeamAssignmentDB(TeamAssignmentCreate):
  id: int
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode = True

class TeamAssignment(TeamAssignmentDB):
  pass