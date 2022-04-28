from typing import List
from fastapi import APIRouter, HTTPException, Depends
from api.deps import get_db, require_active_user
from api.controllers import team_controller
from api import schemas

router = APIRouter()

@router.post("/", response_model=schemas.Team)
def create_team(
  data: schemas.TeamCreate,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  team_exists = team_controller.get_by_name(db, name=data.name)
  if team_exists:
    raise HTTPException(400, "Name in use")
  return team_controller.create(db, obj_in=data)

@router.get("/", response_model=List[schemas.Team])
def list_teams(
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  teams = team_controller.get_many(db)
  if len(teams) == 0:
    raise HTTPException(404, "Teams not found")
  return teams

@router.get("/{id}", response_model=schemas.Team)
def detail_team(
  id: int,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  return team_controller.get_or_404(db, id)

@router.delete("/{id}", response_model=schemas.Team)
def delete_team(
  id: int,
  db = Depends(get_db),
):
  team_controller.get_or_404(db, id, message="Team not found")
  return team_controller.remove(db, id=id)
   
@router.patch("/{id}", response_model=schemas.Team)
def update_team(
  id: int,
  data: schemas.TeamUpdate,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  team = team_controller.get_or_404(db, id, message="Team not found")
  return team_controller.update(db, db_obj=team, obj_in=data)

@router.get("/{id}/members", response_model=List[schemas.PersonDB])
def list_team_members(
  id: int,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  team = team_controller.get_or_404(db, id, message="Team not found")
  if len(team.members) == 0:
    raise HTTPException(404, "Team has no members")
  return team.members

@router.get("/{id}/assignments", response_model=List[schemas.TeamAssignment])
def list_team_assignments(
  id: int,
  db = Depends(get_db),
  user = Depends(require_active_user),
):
  team = team_controller.get_or_404(db, id, message="Team not found")
  if len(team.assignments) == 0:
    raise HTTPException(404, "Team has no assignments")
  return team.assignments