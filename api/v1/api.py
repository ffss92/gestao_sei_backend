from fastapi import APIRouter
from .routes import (
  user,
  person,
  team,
  team_assignment,
  process,
  destination,
  process_update
)

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["Users"])
router.include_router(person.router, prefix="/people", tags=["People"])
router.include_router(team.router, prefix="/teams", tags=["Teams"])
router.include_router(team_assignment.router, prefix="/team-assignments", tags=["Team Assignments"])
router.include_router(process.router, prefix="/processes", tags=["Processes"])
router.include_router(destination.router, prefix="/destinations", tags=["Destinations"])
router.include_router(process_update.router, prefix="/process-updates", tags=["Process Updates"])