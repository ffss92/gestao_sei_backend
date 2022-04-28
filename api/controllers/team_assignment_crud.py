from .base import ControllerBase
from api.schemas import TeamAssignmentCreate, TeamAssignmentUpdate
from api.models import TeamAssignment


class TeamAssignmentController(
    ControllerBase[
      TeamAssignment, 
      TeamAssignmentCreate, 
      TeamAssignmentUpdate
    ]
  ):
  pass

team_assignment_controller = TeamAssignmentController(TeamAssignment)