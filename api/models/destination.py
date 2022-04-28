from datetime import datetime
from api.utils.database import Base
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import relationship
from .process_destination import process_destination_rel


class Destination(Base):
  __tablename__ = "destination"
  id = Column(Integer, primary_key=True)
  name = Column(String(255), unique=True, nullable=False, index=True)
  short_name = Column(String(50), index=True)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  processes = relationship("Process", secondary=process_destination_rel)

  # processes = relationship("Process", back_populates="destination", )