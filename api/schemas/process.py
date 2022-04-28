from pydantic import BaseModel, constr
from datetime import datetime
from typing import List, Optional
from .destination import Destination
from .person import Person
from .user import User
from .process_updates import ProcessUpdates
from .generic import Pagination


ProcessNumber = constr(regex=r"^\d{4}.\d{2}.\d{7}/\d{4}-\d{2}$")

class ProcessCreate(BaseModel):
  number: ProcessNumber
  is_active: Optional[bool] = None
  is_generated: Optional[bool] = None
  subject: str
  description: Optional[str] = None
  person_id: Optional[int] = None
  origin_id: Optional[int] = None
  due_to: Optional[datetime] = None
  destination_ids: Optional[List[int]] = None
  
  

class ProcessUpdate(BaseModel):
  number: Optional[ProcessNumber] = None
  subject: Optional[str] = None
  description: Optional[str] = None
  person_id: Optional[int] = None
  origin_id: Optional[int] = None
  is_active: Optional[bool] = None
  is_generated: Optional[bool] = None
  due_to: Optional[datetime] = None
  destination_ids: Optional[List[int]] = None

class ProcessDB(BaseModel):
  id: int
  number: ProcessNumber
  is_active: Optional[bool] = None
  is_generated: Optional[bool] = None
  subject: str
  description: Optional[str] = None
  person_id: Optional[int] = None
  origin_id: Optional[int] = None
  due_to: Optional[datetime] = None
  created_at: datetime
  updated_at: Optional[datetime] = None
  created_by: Optional[int] = None

  class Config:
    orm_mode = True

class Process(ProcessDB):
  user: Optional[User] = None
  responsible: Optional[Person] = None
  origin: Optional[Destination] = None
  updates: Optional[List[ProcessUpdates]] = None
  destinations: Optional[List[Destination]] = None

class ProcessList(BaseModel):
  meta: Pagination
  data: List[Process]
  