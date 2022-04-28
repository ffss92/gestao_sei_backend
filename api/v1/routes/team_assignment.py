from typing import List
from fastapi import APIRouter, HTTPException, Depends
from api.controllers import (
  team_assignment_controller, 
  team_controller,
)
from api import schemas
from api.deps import get_db, require_active_user


router = APIRouter()

@router.post("/", response_model=schemas.TeamAssignment)
def create_team_assignment(
  data: schemas.TeamAssignmentCreate,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  team_controller.get_or_404(db, id=data.team_id, message="Team not found")
  return team_assignment_controller.create(db, obj_in=data)

@router.get("/", response_model=List[schemas.TeamAssignment])
def list_team_assignments(
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  assignments = team_assignment_controller.get_many(db, limit=1000)
  if len(assignments) == 0:
    raise HTTPException(404, "Team assignments not found")
  return assignments

@router.get("/{id}", response_model=schemas.TeamAssignment)
def detail_team_assignment(
  id: int,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  return team_assignment_controller.get_or_404(
    db, 
    id=id, 
    message="Team assignment not found"
  )

@router.delete("/{id}", response_model=schemas.TeamAssignment)
def delete_team_assignment(
  id: int,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  team_assignment_controller.get_or_404(
    db,
    id=id,
    message="Team assingment not found",
  )
  return team_assignment_controller.remove(db, id=id)

@router.patch("/{id}", response_model=schemas.TeamAssignment)
def update_team_assignment(
  id: int,
  data: schemas.TeamAssignmentUpdate,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  assignment = team_assignment_controller.get_or_404(
    db,
    id=id,
    message="Team assingment not found",
  )
  return team_assignment_controller.update(db, db_obj=assignment, obj_in=data)
