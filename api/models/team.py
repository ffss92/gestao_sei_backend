from api.utils.database import Base
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship


class Team(Base):
  __tablename__ = "team"

  id = Column(Integer, primary_key=True)
  name = Column(String(255), nullable=False, unique=True)
  description = Column(String(255))
  is_active = Column(Boolean, default=True)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  members = relationship("Person", back_populates="team")
  assignments = relationship("TeamAssignment", back_populates="team", cascade="all, delete")
