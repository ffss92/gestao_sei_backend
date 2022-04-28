from .base import ControllerBase
from api.models import Person
from api.schemas import PersonCreate, PersonUpdate
from sqlalchemy.orm import Session


class PersonController(ControllerBase[Person, PersonCreate, PersonUpdate]):

  def get_by_email(self, db: Session, *, email: str):
    return db.query(self.model).filter_by(professional_email=email).first()

  def get_by_user_id(self, db: Session, *, user_id: int):
    return db.query(self.model).filter_by(user_id=user_id).first()

  def get_by_team_status(self, db: Session, *, has_team: bool):
    if has_team:
      return db.query(self.model).filter(self.model.team_id != None).all()
    return db.query(self.model).filter(self.model.team_id == None).all()
    

person_controller = PersonController(Person)

