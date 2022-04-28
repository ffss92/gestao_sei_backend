from api.utils.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship


class Person(Base):
  __tablename__ = "person"

  id = Column(Integer, primary_key=True)
  full_name = Column(String(255), nullable=False, index=True)
  phone_number = Column(String(255))
  professional_email = Column(String(255), nullable=False, unique=True)
  is_active = Column(Boolean, default=True)
  work_phone = Column(String(255))
  on_vacation = Column(Boolean, default=False)
  user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), unique=True)
  team_id = Column(Integer, ForeignKey("team.id", ondelete="SET NULL"))
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  user = relationship("User", back_populates="person")
  team = relationship("Team", back_populates="members")
  processes = relationship("Process", back_populates="responsible")
