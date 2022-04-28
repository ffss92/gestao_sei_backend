from sqlalchemy.orm import Session
from typing import List, TypeVar, Generic, Type, Optional, Any, Union, Dict
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from api.utils.database import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class ControllerBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
  def __init__(self, model: Type[ModelType]) -> None:
    self.model = model

  def count(self, db: Session, **kwargs) -> int:
    additional_query = {}
    for key, value in kwargs.items():
      if value is not None:
        additional_query[key] = value
    if additional_query:
      return db.query(self.model).filter_by(**additional_query).count()
    return db.query(self.model).count()
  
  def get(self, db: Session, id: Any) -> Optional[ModelType]:
    return db.query(self.model).filter(self.model.id == id).first()

  def get_or_404(self, db: Session, id: Any, *, message: str = "Not found") -> ModelType:
    result = self.get(db, id)
    if not result:
      raise HTTPException(404, message)
    return result

  def get_many(
    self, db: Session, *, skip: int = 0, limit: int = 100, **kwargs
  ) -> List[ModelType]:
    additional_query = {}
    for key, value in kwargs.items():
      if value is not None:
        additional_query[key] = value
    if additional_query:
      return db.query(self.model).filter_by(**additional_query).offset(skip).limit(limit).all()
    return db.query(self.model).offset(skip).limit(limit).all()

  def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = self.model(**obj_in_data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def update(
    self,
    db: Session,
    *,
    db_obj: ModelType,
    obj_in: Union[UpdateSchemaType, Dict[str, Any]]
  ) -> ModelType:
    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in, dict):
      update_data = obj_in
    else:
      update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
      if field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def remove(self, db: Session, *, id: int) -> ModelType:
    obj = db.query(self.model).get(id)
    db.delete(obj)
    db.commit()
    return obj

class AuthControllerBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
  def __init__(self, model: Type[ModelType]) -> None:
    self.model = model
  
  def get(self, db: Session, id: int, user_id: int) -> Optional[ModelType]:
    return db.query(self.model).filter_by(id = id, user_id=user_id).first()

  def get_many(
    self, db: Session, *, skip: int = 0, limit: int = 100, user_id: int
  ) -> List[ModelType]:
    return db.query(self.model).filter_by(user_id=user_id).offset(skip).limit(limit).all()

  def create(self, db: Session, *, obj_in: CreateSchemaType, user_id: int) -> ModelType:
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = self.model(**obj_in_data, user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def update(
    self,
    db: Session,
    *,
    db_obj: ModelType,
    obj_in: Union[UpdateSchemaType, Dict[str, Any]]
  ) -> ModelType:
    obj_data = jsonable_encoder(db_obj)
    if isinstance(obj_in, dict):
      update_data = obj_in
    else:
      update_data = obj_in.dict(exclude_unset=True)
    for field in obj_data:
      if field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def remove(self, db: Session, *, id: int, user_id: int) -> ModelType:
    obj = db.query(self.model).filter_by(id = id, user_id = user_id).first()
    db.delete(obj)
    db.commit()
    return obj