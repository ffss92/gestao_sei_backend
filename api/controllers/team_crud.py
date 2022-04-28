from .base import ControllerBase
from api.models import Team
from api.schemas import TeamUpdate, TeamCreate
from sqlalchemy.orm import Session
# from sqlalchemy.orm import Session


class TeamController(ControllerBase[Team, TeamCreate, TeamUpdate]):
  
  def get_by_name(self, db: Session, *, name: str):
    return db.query(self.model).filter_by(name=name).first()

team_controller = TeamController(Team)

