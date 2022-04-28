from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class DestinationCreate(BaseModel):
  name: str
  short_name: Optional[str] = None

class DestinationUpdate(BaseModel):
  name: Optional[str] = None
  short_name: Optional[str] = None

class DestinationDB(DestinationCreate):
  id: int
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode = True

class Destination(DestinationDB):
  pass