from datetime import datetime
from typing import List
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.functions import func
from .base import ControllerBase
from api.schemas import ProcessUpdate, ProcessCreate
from api.models import Process, Destination, Person, User, process_destination_rel
from sqlalchemy.orm import Session
from sqlalchemy import or_, extract
from fastapi.encoders import jsonable_encoder


class ProcessController(ControllerBase[Process, ProcessCreate, ProcessUpdate]):

  def search_all(self, db: Session, *, value: str, limit: int = 100, skip: int = 0):
    destination_subquery = db.query(Destination.id).filter(
      or_(
        Destination.name.ilike(f"%{value}%"), 
        Destination.short_name.ilike(f"%{value}%")
      )
    )
    person_subquery = db.query(Person.id).filter(Person.full_name.ilike(f"%{value}%"))
    user_subquery = db.query(User.id).filter(User.email.ilike(f"%{value}%"))
    query = or_(
        self.model.number.ilike(f"%{value}%"),
        self.model.description.ilike(f"%{value}%"),
        self.model.subject.ilike(f"%{value}%"),
        self.model.origin_id.in_(destination_subquery),
        self.model.person_id.in_(person_subquery),
        self.model.created_by.in_(user_subquery),
      )
    count = db.query(self.model).filter(query).count()
    return db.query(self.model).filter(query).order_by(self.model.created_at.desc()).limit(limit).offset(skip).all(), count

  def advanced_search(
    self, 
    db: Session, 
    *, 
    date: datetime,
    limit: int = 100, 
    skip: int = 0,
    **kwargs,
    ):
    and_express = []
    has_destination_id = False # Confere se há necessidade de pesquisar destino
    destination_id = 0
    for key, value in kwargs.items():
      if key == "person_id" and value is not None:
        and_express.append(self.model.person_id == value)
        continue
      if key == "origin_id" and value is not None:
        and_express.append(self.model.origin_id == value)
        continue
      if key == "destination_id" and value is not None:
        has_destination_id = True
        destination_id = value
        continue
      if value is not None:
        and_express.append(getattr(self.model, key).ilike(f"%{value}%"))

    q = db.query(self.model).filter(and_(*and_express)).order_by(self.model.created_at.desc())
   
    if date is not None:
      date_query = and_(
        extract("month", self.model.created_at) == date.month,
        extract("year", self.model.created_at) == date.year,
      )
      q = q.filter(date_query)
    
    if has_destination_id:
      q = q.filter(self.model.destinations.any(id=destination_id))

    count = q.count() # Conta o número de registros antes de aplicar paginação
    q = q.limit(limit).offset(skip) # Aplica paginação
    results = q.all() # Executa a query

    return results, count

  def create(self, db: Session, *, obj_in: ProcessCreate, user_id: int):
    obj_in_data = jsonable_encoder(obj_in)
    db_obj = self.model(**obj_in_data, created_by=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

  def get_many(
    self, db: Session, *, skip: int = 0, limit: int = 100, **kwargs
  ) -> List[Process]:
    additional_query = {}
    for key, value in kwargs.items():
      if value is not None:
        additional_query[key] = value
    if additional_query:
      return db.query(self.model).filter_by(**additional_query).order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()
    return db.query(self.model).order_by(self.model.created_at.desc()).offset(skip).limit(limit).all()

  def get_by_number(self, db: Session, *, number: str):
    return db.query(self.model).filter_by(number=number).first()

  def latest(self, db: Session):
    return db.query(self.model).order_by(self.model.created_at.desc()).limit(5).all()

  def add_destinations(self, db: Session, db_obj: Process, destinations: List[Destination]):
    db_obj.destinations = destinations
    db.commit()

  def user_month_total(self, db: Session, date: datetime, user: User):
    query = and_(
        extract("month", self.model.created_at) == date.month,
        extract("year", self.model.created_at) == date.year,
        self.model.created_by == user.id,
      )
    return db.query(self.model).filter(query).count()

  def month_total(self, db: Session, date: datetime):
    query = and_(
      extract("month", self.model.created_at) == date.month,
      extract("year", self.model.created_at) == date.year,
    )
    return db.query(self.model).filter(query).count()

  def total_by_month(self, db: Session, date: datetime):
    return db.query(
      func.count(self.model.id).label("total"), 
      func.month(self.model.created_at).label("month"),
      ).group_by(
      func.month(self.model.created_at),
    ).filter(extract("year", self.model.created_at) == date.year).all()

process_controller = ProcessController(Process)