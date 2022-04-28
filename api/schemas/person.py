from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, constr
from api.schemas.team import Team
# from api.schemas.user import User


PhoneNumber = constr(regex=r"^\(\d{2}\) \d{4,5}-\d{4}$")
WorkPhone = constr(regex=r"^\d{5}")

class PersonCreate(BaseModel):
  full_name: str
  is_active: Optional[bool] = None
  phone_number: Optional[PhoneNumber] = None
  professional_email: EmailStr
  user_id: Optional[int] = None
  team_id: Optional[int] = None
  work_phone: Optional[WorkPhone] = None
  on_vacation: Optional[bool] = None

class PersonUpdate(PersonCreate):
  professional_email: Optional[EmailStr] = None
  full_name: Optional[str] = None
  work_phone: Optional[WorkPhone] = None
  on_vacation: Optional[bool] = None

class PersonDB(PersonCreate):
  id: int
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode = True

class Person(PersonDB):
  team: Optional[Team] = None
  # user: Optional[User] = None