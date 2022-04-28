from typing import List
from fastapi import APIRouter, Depends, HTTPException
from api.deps import get_db, require_active_user
from api import schemas
from api.controllers import destination_controller
from api.utils import event_publisher


router = APIRouter()

not_found_message = "Destination not found"

@router.post("/", response_model=schemas.Destination)
def create_destination(
  data: schemas.DestinationCreate,
  db = Depends(get_db),
  user = Depends(require_active_user)
):
  
  destination_exists = destination_controller.get_by_name(db, name=data.name)
  if destination_exists:
    raise HTTPException(400, "Name in use")
  new_destination = destination_controller.create(db, obj_in=data)
  event_publisher.destination_event(type_="created", db_obj=new_destination, user=user)
  return new_destination

@router.get("/", response_model=List[schemas.Destination])
def list_destinations(
  db = Depends(get_db),
):
  destinations = destination_controller.get_many(db, limit=1000)
  if len(destinations) == 0:
    raise HTTPException(404, "Destinations not found")
  return destinations

@router.get("/{id}", response_model=schemas.Destination)
def detail_destination(
  id: int,
  db = Depends(get_db),
):
  return destination_controller.get_or_404(
    db, 
    id=id, 
    message=not_found_message
  )

@router.delete("/{id}", response_model=schemas.Destination)
def delete_destination(
  id: int,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  destination_controller.get_or_404(
    db, 
    id=id,
    message=not_found_message
  )
  deleted_destination = destination_controller.remove(db, id=id)
  event_publisher.destination_event(type_="deleted", db_obj=deleted_destination, user=user)
  return deleted_destination

@router.patch("/{id}", response_model=schemas.Destination)
def update_destination(
  id: int,
  data: schemas.DestinationUpdate,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  destination = destination_controller.get_or_404(
    db, 
    id=id, 
    message=not_found_message
  )
  updated_destination = destination_controller.update(
    db,
    db_obj=destination,
    obj_in=data,
  )
  event_publisher.destination_event(type_="updated", db_obj=updated_destination, user=user)
  return updated_destination
