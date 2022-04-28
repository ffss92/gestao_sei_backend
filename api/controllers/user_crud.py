from typing import Union, Optional
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from api.models.user import User
from api.schemas.user import UserCreate, UserUpdate
from api.core.security import verify_pw, hash_pw
from .base import ControllerBase


class UserController(ControllerBase[User, UserCreate, UserUpdate]):

  def get_by_email(self, db: Session, email: str) -> Optional[User]:
    return db.query(self.model).filter(self.model.email == email).first()

  def create(self, db: Session, *, obj_in: UserCreate) -> User:
    hashed_pw = hash_pw(obj_in.password)
    user = User(email=obj_in.email, password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

  def create_admin(self, db: Session, *, obj_in: UserCreate) -> User:
    """Cria o administrador do sistema."""
    hashed_pw = hash_pw(obj_in.password)
    user = User(email=obj_in.email, password=hashed_pw, is_admin=True, is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

  def authenticate(self, db: Session, *, obj_in: OAuth2PasswordRequestForm) -> Union[User, None]:
    """Autentica o usuário com base nas credenciais oferecidas."""
    user = self.get_by_email(email=obj_in.username, db=db)
    if not user:
      return None
    if not verify_pw(obj_in.password, user.password):
      return None
    return user


user_controller = UserController(User)

