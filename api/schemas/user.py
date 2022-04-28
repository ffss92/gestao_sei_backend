from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from .person import PersonDB


class UserBase(BaseModel):
  """Representação base do Usuário"""
  email: Optional[EmailStr] = None
  is_active: Optional[bool] = True
  is_admin: bool = False
  created_at: datetime
  updated_at: datetime


class UserCreate(BaseModel):
  """Representação de criação de Usuários"""
  email: EmailStr
  password: str

  @validator("password")
  def pw_len(cls, v):
    """Valida o tamanho da senha do usuário - Mínimo 8 caracteres"""
    if len(v) < 8:
      raise ValueError("Password must contain at least 8 characters")
    return v


class UserUpdate(BaseModel):
  """Representação de atualização de Usuários"""
  is_active: Optional[bool] = None
  is_admin: Optional[bool] = None


class UserDBBase(UserBase):
  """Representação de Usuários no banco de dados"""
  id: int

  class Config:
    orm_mode = True


class UserChangePassword(BaseModel):
  password: str
  new_password: str


class User(UserDBBase):
  """Representação de Usuários no banco de dados com informações adicionais """
  # person: Optional[PersonDB] = None