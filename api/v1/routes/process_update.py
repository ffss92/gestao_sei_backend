from typing import List
from api import models, schemas
from api.controllers import process_controller, process_update_controller
from api.deps import get_db, require_active_user
from fastapi import HTTPException, Depends, APIRouter


router = APIRouter()

@router.post("/", response_model=schemas.ProcessUpdates)
def create_process_update(
  data: schemas.ProcessUpdatesCreate,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  process_controller.get_or_404(db, id=data.process_id, message="Process not found")
  return process_update_controller.create(db, obj_in=data, user_id=user.id)

@router.get("/", response_model=List[schemas.ProcessUpdates])
def list_process_updates(
  db = Depends(get_db),
  _ = Depends(require_active_user),
):
  process_updates = process_update_controller.get_many(db, limit=1000)
  if len(process_updates) == 0:
    raise HTTPException(404, "Proccess updates not found")
  return process_updates

@router.delete("/{id}", response_model=schemas.ProcessUpdates)
def delete_process_update(
  id: int,
  db = Depends(get_db),
  user: models.User = Depends(require_active_user),
):
  process_update = process_update_controller.get_or_404(db, id=id, message="Process update not found")
  if not user.is_admin:
    if user.id != process_update.user_id:
      raise HTTPException(403, "Forbidden")
  return process_update_controller.remove(db, id=id)

@router.patch("/{id}", response_model=schemas.ProcessUpdates)
def update_process_update(
  id: int,
  data: schemas.ProcessUpdatesUpdate,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  process_update = process_update_controller.get_or_404(db, id=id, message="Process update not found")
  if not user.is_admin:
    if user.id != process_update.user_id:
      raise HTTPException(403, "Forbidden")
  return process_update_controller.update(db, db_obj=process_update, obj_in=data)
