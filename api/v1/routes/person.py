from typing import List, Optional
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from api import schemas
from api.controllers import (
  person_controller, 
  team_controller,
  user_controller,
)
from api.deps import get_db, require_active_user

router = APIRouter()

@router.post("/", response_model=schemas.Person)
def create_person(
  data: schemas.PersonCreate,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  """Cadastra uma nova pessoa"""
  # Verifica se já há uma pessoa com o email insitucional cadastrado
  email_exists = person_controller.get_by_email(db, email=data.professional_email)
  if email_exists:
    raise HTTPException(400, "Email in use")

  # Se informado um id de Team, confirmar a existência
  if data.team_id is not None:
    team_controller.get_or_404(db, data.team_id, message="Team not found")

  # Se informado um id de User, confirmar a existência
  if data.user_id is not None:
    user_controller.get_or_404(db, data.user_id, message="User not found")

    # Verifica se já há um usuário vinculado à pessoa
    if person_controller.get_by_user_id(db, user_id=data.user_id):
      raise HTTPException(400, "User in use")

  # Criar
  return person_controller.create(db, obj_in=data)


@router.get("/", response_model=List[schemas.Person])
def list_people(
  has_team: Optional[bool] = None,
  has_user: Optional[bool] = None,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  """Retorna uma lista de pessoas"""
  # Verifica se a query 'has_team' foi passada
  if has_team is not None:
    people = person_controller.get_by_team_status(db, has_team=has_team)
    # Verifica se foi retornado ao menos um objeto
    if len(people) == 0:
      raise HTTPException(404, "People not found")
    return people
  people = person_controller.get_many(db, skip=0, limit=100, has_user=has_user)
  # Verifica se foi retornado ao menos um objeto
  if len(people) == 0:
    raise HTTPException(404, "People not found")
  return people


@router.get("/{id}", response_model=schemas.Person)
def detail_person(
  id: int, 
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  """Retorna uma pessoa com base no id fornecido"""
  return person_controller.get_or_404(db, id)


@router.delete("/{id}", response_model=schemas.Person)
def delete_person(
  id: int,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  """Remove uma pessoas com base no id fornecido"""
  person_controller.get_or_404(db, id)
  deleted_person = person_controller.remove(db, id=id)    
  return deleted_person

@router.patch("/{id}", response_model=schemas.Person)
def update_person(
  id: int,
  data: schemas.PersonUpdate,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  """Atualiza os dados de uma pessoa"""
  person = person_controller.get_or_404(db, id)

  # Se informado um id de Team, confirmar a existência
  if data.team_id is not None:
    team_controller.get_or_404(db, data.team_id, message="Team not found")

  # Se informado um id de User, confirmar a existência
  if data.user_id is not None:
    user_controller.get_or_404(db, data.user_id, message="User not found")

    # Verifica se já há um usuário vinculado à pessoa
    if person_controller.get_by_user_id(db, user_id=data.user_id):
      raise HTTPException(400, "User in use")

  # Atualiza os dados
  updated_person = person_controller.update(db, db_obj=person, obj_in=data)
  return updated_person

@router.get("/{id}/processes", response_model=List[schemas.Process])
def list_person_processes(
  id: int,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  person = person_controller.get_or_404(db, id=id, message="Person not found")
  if len(person.processes) == 0:
    raise HTTPException(404, "Person has no processes")
  return person.processes