from typing import List
from sqlalchemy.orm.session import Session
from .base import ControllerBase
from api import schemas, models

class DestinationController(ControllerBase[
  models.Destination, 
  schemas.DestinationCreate, 
  schemas.DestinationUpdate
]):
  def get_by_name(self, db: Session, *, name: str):
    return db.query(self.model).filter_by(name=name).first()

  def get_many(
    self, db: Session, *, skip: int = 0, limit: int = 500,
  ) -> List[models.Destination]:
    return db.query(self.model).order_by(self.model.name.asc()).all()

destination_controller = DestinationController(models.Destination)