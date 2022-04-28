from typing import List, Optional
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from api import schemas, models
from api.controllers import user_controller
from api.deps import get_db, require_active_user, require_admin
from api.core.security import create_access_token, hash_pw, verify_pw


router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login_access_token(
  db = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends(),
):
  """Gera um novo token de acesso JWT."""
  user = user_controller.authenticate(db=db, obj_in=form_data)
  if not user:
    raise HTTPException(400, "E-mail or password is invalid")
  if not user.is_active:
    raise HTTPException(401, "User is no longer active")
  return {
    "access_token": create_access_token(user.id),
    "token_type": "bearer",
  }

@router.post("/", response_model=schemas.User)
def create_user(
    data: schemas.UserCreate, 
    db = Depends(get_db),
  ):
  """Cria um novo usuário."""
  user = user_controller.get_by_email(db=db, email=data.email)
  # Verifica se já existe um usuário com o e-mail
  if user:
    raise HTTPException(400, "E-mail in use")
  user = user_controller.create(db=db, obj_in=data)
  return user

@router.get("/", response_model=List[schemas.User])
def read_users(
    is_active: Optional[bool] = None,
    is_admin: Optional[bool] = None,
    db = Depends(get_db), 
    _ = Depends(require_active_user),
  ):
  """Retorna lista de usuários."""
  users = user_controller.get_many(
    db=db,
    is_active=is_active,
    is_admin=is_admin,
  )
  if len(users) == 0:
    raise HTTPException(404, "Not found")
  return users

@router.get("/me", response_model=schemas.User)
def current_user(
  user = Depends(require_active_user),
  ):
  """Retorna informações do usuário logado."""
  return user

@router.patch("/change-password")
def change_user_password(
  data: schemas.UserChangePassword,
  db = Depends(get_db),
  current_user: models.User = Depends(require_active_user),
):
  password_valid = verify_pw(data.password, current_user.password)
  if not password_valid:
    raise HTTPException(400, "Password is invalid")
  new_password_hash = hash_pw(data.new_password)
  updated_user = user_controller.update(db, db_obj=current_user, obj_in={"password": new_password_hash})
  return updated_user

@router.patch("/{id}", response_model=schemas.User)
def update_user(
  id: int,
  data: schemas.UserUpdate,
  db = Depends(get_db),
  current_user: models.User = Depends(require_active_user),
):

  # Verifica se os campos 'is_active' e 'is_admin' estão tentando ser modificados
  if data.is_active != None or data.is_admin != None:
    if current_user.is_admin == False:
      raise HTTPException(403, "Forbidden")
  user = user_controller.get_or_404(db, id, message="User not found")
  
  # Verifica o usuário atual é quem está tentando fazer a modificação
  # caso não haja solicitação de mudança de senha
  if user.id != current_user.id:
    if current_user.is_admin == False:
      raise HTTPException(403, "Forbidden")

  updated_user = user_controller.update(db, db_obj=user, obj_in=data)
  return updated_user

