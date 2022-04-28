from datetime import date, datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from api import schemas
from api.controllers import (
  person_controller, 
  process_controller, 
  destination_controller
)
from api.deps import get_db, require_active_user
from math import ceil
from api.utils import event_publisher

router = APIRouter()

@router.post("/", response_model=schemas.Process)
def create_process(
  data: schemas.ProcessCreate,
  db = Depends(get_db),
  user = Depends(require_active_user)
):
  """Registra um novo processo SEI"""
  process_exits = process_controller.get_by_number(db, number=data.number)
  
  # Verifica se já existe um processo com o número informado
  if process_exits:
    raise HTTPException(400, "Process already registered")
  
  # Se um responsável for informado, verifica a sua existência
  if data.person_id:
    person_controller.get_or_404(db, id=data.person_id, message="Person not found")

  # Se uma origem for informado, verifica sua existência
  if data.origin_id:
    destination_controller.get_or_404(db, id=data.origin_id, message="Origin not found")

  destinations = []

  if data.destination_ids:
    destinations = [destination_controller.get_or_404(db, id=id, message="Destination not found") for id in data.destination_ids]
  insert_data = data.copy(exclude={"destination_ids"})
  # Caso tudo esteja ok, cria o processo
  new_process = process_controller.create(db, obj_in=insert_data, user_id=user.id)

  if destinations:
    process_controller.add_destinations(db, db_obj=new_process, destinations=destinations)

  return new_process

@router.get("/", response_model=schemas.ProcessList)
def list_processes(
  q: Optional[str] = None,
  is_active: Optional[bool] = None,
  created_by: Optional[int] = None,
  limit: Optional[int] = Query(ge=1, le=100, default=50),
  page: Optional[int] = Query(ge=1, default=1),
  db = Depends(get_db)
):
  """Lista os processos SEI registrados"""
  # Busca os processos que contenham 'q'
  if q is not None:
    processes, count = process_controller.search_all(db, value=q, limit=limit, skip=(page -1 ) * limit)
    if not processes:
      raise HTTPException(404, "Processes not found")
    return {
      "meta": {
        "current_page": page,
        "total_pages": ceil(count / limit),
        "count": count,
        "limit": limit
      },
      "data": processes
    }
  # Lista os processos
  processes = process_controller.get_many(
    db, 
    limit=limit, 
    skip=(page -1 ) * limit,
    created_by=created_by,
    is_active=is_active
  )
  count = process_controller.count(
    db=db,
    created_by=created_by,
    is_active=is_active
  )
  if len(processes) == 0:
    raise HTTPException(404, "Processes not found")
  return {
    "meta": {
      "current_page": page,
      "total_pages": ceil(count / limit),
      "count": count,
      "limit": limit
    },
    "data": processes
  }

@router.get("/advanced", response_model=schemas.ProcessList)
def advanced_search(
  subject: Optional[str] = None,
  description: Optional[str] = None,
  created_by: Optional[int] = None,
  person_id: Optional[int] = None,
  destination_id: Optional[int] = None,
  origin_id: Optional[int] = None,
  date: Optional[datetime] = None,
  limit: Optional[int] = Query(ge=1, le=100, default=50),
  page: Optional[int] = Query(ge=1, default=1),
  db = Depends(get_db),
):
  results, count = process_controller.advanced_search(
    db, 
    subject=subject,
    created_by=created_by,
    person_id=person_id,
    destination_id=destination_id,
    origin_id=origin_id,
    limit=limit, 
    skip=(page - 1) * limit, 
    date=date,
    description=description,
  )
  if len(results) == 0:
    raise HTTPException(404, "Processes not found")
  return {
    "meta": {
      "current_page": page,
      "total_pages": ceil(count / limit),
      "count": count,
      "limit": limit
    },
    "data": results
  }

@router.get("/latest", response_model=List[schemas.Process])
def latest_processes(
  db = Depends(get_db)
):
  """Retorna os últimos 10 processos"""
  latest = process_controller.latest(db)
  if len(latest) == 0:
    raise HTTPException(404, "Processes not found")
  return latest

@router.get("/info")
def dashboard_info(
  date: Optional[datetime] = None,
  user = Depends(require_active_user),
  db = Depends(get_db),
):
  user_count = process_controller.user_month_total(db, date=date, user=user)
  total_count = process_controller.month_total(db, date=date)
  return {
    "user_count": user_count,
    "total_count": total_count,
  }

@router.get("/{id}", response_model=schemas.Process)
def detail_process(
  id: int,
  db = Depends(get_db)
):
  """Retorna os detalhes de um processo SEI com base no id fornecido"""
  return process_controller.get_or_404(db, id=id, message="Process not found")

@router.delete("/{id}", response_model=schemas.Process)
def delete_process(
  id: int,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  """Remove um processo SEI com base no id fornecido"""
  process = process_controller.get_or_404(db, id=id, message="Process not found")
  if not user.is_admin:
    if process.created_by != user.id:
      raise HTTPException(403, "Forbidden")
  deleted_process = process_controller.remove(db, id=id)
  event_publisher.process_event(type_="deleted", db_obj=deleted_process, user=user)
  return deleted_process

@router.patch("/{id}", response_model=schemas.Process)
def update_process(
  id: int,
  data: schemas.ProcessUpdate,
  db = Depends(get_db),
  _ = Depends(require_active_user)
):
  """Atualiza um processo SEI com base no id fornecido"""
  process = process_controller.get_or_404(db, id=id, message="Process not found")

  if data.number != process.number:
    process_exists = process_controller.get_by_number(db, number=data.number)
    if process_exists:
      raise HTTPException(400, "Number in use")

  # Se um responsável for informado, verifica a sua existência
  if data.person_id:
    person_controller.get_or_404(db, id=data.person_id, message="Person not found")

  # Se uma origem for informado, verifica sua existência
  if data.origin_id:
    destination_controller.get_or_404(db, id=data.origin_id, message="Origin not found")

  destinations = []

  if data.destination_ids:
    destinations = [destination_controller.get_or_404(db, id=id, message="Destination not found") for id in data.destination_ids]

  updated_process = process_controller.update(db, db_obj=process, obj_in=data)
  
  if data.destination_ids is not None:
    process_controller.add_destinations(db, db_obj=updated_process, destinations=destinations)
  
  return updated_process