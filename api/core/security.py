from datetime import timedelta, datetime
from typing import Union, Any
from passlib.context import CryptContext
from . import settings
from jose import jwt


pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pw(password: str) -> str:
  """Faz o hash da senha usando Bcrypt"""
  return pw_context.hash(password)

def verify_pw(password: str, hash: str) -> bool:
  """Verifica se o hash é equivalente à senha fornecida"""
  return pw_context.verify(password, hash)

def create_access_token(sub: Union[str, Any], expire_time: timedelta = settings.TOKEN_EXPIRATION) -> str:
  """Cria um token de acesso JWT"""
  expires = datetime.utcnow() + expire_time
  claims = {"sub": str(sub), "exp": expires}
  access_token = jwt.encode(claims, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
  return access_token