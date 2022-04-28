from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from .user import User


class ProcessUpdatesCreate(BaseModel):
  description: str
  process_id: int

class ProcessUpdatesUpdate(BaseModel):
  description: Optional[str] = None

class ProcessUpdatesDB(ProcessUpdatesCreate):
  id: int
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode = True

class ProcessUpdates(ProcessUpdatesDB):
  user: Optional[User] = None