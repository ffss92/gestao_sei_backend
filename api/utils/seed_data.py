from sqlalchemy.orm import Session
from api.controllers import user_controller
from api.core.settings import settings
from api.schemas import UserCreate


def init_db(db: Session) -> None:
  """Cria um administrador do sistema"""
  user = user_controller.get_by_email(db=db, email=settings.ADMIN_EMAIL)
  if not user:
    user_data = UserCreate(
      email = settings.ADMIN_EMAIL, 
      password = settings.ADMIN_PASSWORD
    )
    user_controller.create_admin(
      db=db, 
      obj_in=user_data
    )