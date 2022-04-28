from .base import ControllerBase, ModelType, CreateSchemaType, jsonable_encoder
from api import models, schemas
from sqlalchemy.orm import Session

class ProcessUpdateController(ControllerBase[
  models.ProcessUpdate,
  schemas.ProcessUpdatesCreate,
  schemas.ProcessUpdatesUpdate,
]):
  def create(self, db: Session, *, obj_in: schemas.ProcessUpdatesCreate, user_id: int) -> models.ProcessUpdate:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = self.model(**obj_in_data, user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

process_update_controller = ProcessUpdateController(models.ProcessUpdate)