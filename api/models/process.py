from api.utils.database import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .process_destination import process_destination_rel


class Process(Base):
  __tablename__ = "process"
  id = Column(Integer, primary_key=True)
  number = Column(String(255), nullable=False, unique=True, index=True)
  is_active = Column(Boolean, default=True)
  is_generated = Column(Boolean, default=False)
  subject = Column(String(600), nullable=False, index=True)
  description = Column(String(600), index=True)
  person_id = Column(Integer, ForeignKey("person.id", ondelete="SET NULL"))
  # destination_id = Column(Integer, ForeignKey("destination.id", ondelete="SET NULL"))
  origin_id = Column(Integer, ForeignKey("destination.id", ondelete="SET NULL"))
  created_by = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))
  due_to = Column(DateTime)
  created_at = Column(DateTime, default=datetime.now, index=True)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  user = relationship("User", backref="processes")
  responsible = relationship("Person", back_populates="processes")
  # destination = relationship("Destination", backref="processes_destinations", foreign_keys=[destination_id])
  destinations = relationship("Destination", secondary=process_destination_rel, back_populates="processes")
  origin = relationship("Destination", backref="processes_origins" , foreign_keys=[origin_id])
  updates = relationship("ProcessUpdate", back_populates="process", cascade="all, delete")
