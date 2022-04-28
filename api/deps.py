from typing import Generator

from jose import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from .utils.database import SessionLocal
from .models.user import User
from .core.settings import settings
from .controllers import user_controller


oauth2 = OAuth2PasswordBearer(
  tokenUrl=f"/api/v1/users/login",
)

def get_db() -> Generator:
  """Cria uma sessão com o banco de dados."""
  try:
    db: Session = SessionLocal()
    yield db
  finally:
    db.close()

def require_auth(db: Session = Depends(get_db), token: str = Depends(oauth2)) -> User:
  """Decodifica o chave de acesso JWT e retorna o usuário."""
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
  except (jwt.JWTError, ValidationError):
    raise HTTPException(401, "Access Denied")
  user = user_controller.get(db=db, id=payload.get("sub"))
  if not user:
    raise HTTPException(404, "User not found")
  return user

def require_active_user(user: User = Depends(require_auth)) -> User:
  """Verfica se `user.is_active` retorna `True`."""
  if not user.is_active:
    raise HTTPException(400, "User is not active")
  return user

def require_admin(user: User = Depends(require_active_user)) -> User:
  """Verfica se `user.is_admin` retorna `True`."""
  if not user.is_admin:
    raise HTTPException(403, "Unauthorized")
  return user

def pagination_args(page: int = Query(1, gt=0), limit: int = Query(20, gt=0, le=40)):
  """Adiciona os parâmetros `page` e `limit` à query do endpoint e retorna um dicinionário de chaves com o mesmo nome."""
  return {"page": page, "limit": limit}
