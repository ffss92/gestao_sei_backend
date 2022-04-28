from sqlalchemy.orm import relationship
from api.utils.database import Base
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from datetime import datetime


class TeamAssignment(Base):
  __tablename__ = "team_assignment"
  id = Column(Integer, primary_key=True)
  description = Column(String(255), nullable=False)
  team_id = Column(Integer, ForeignKey("team.id", ondelete="CASCADE"), nullable=False)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  team = relationship("Team", back_populates="assignments")