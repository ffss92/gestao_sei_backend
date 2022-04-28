from api.utils.database import Base
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):
  __tablename__ = "user"
  
  id = Column(Integer, primary_key=True)
  email = Column(String(255), nullable=False, unique=True)
  password = Column(String(255), nullable=False)
  is_admin = Column(Boolean, default=False, nullable=False)
  is_active = Column(Boolean, default=False, nullable=False)
  created_at = Column(DateTime(), default=datetime.now)
  updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

  person = relationship("Person", back_populates="user")
  process_updates = relationship("ProcessUpdate", back_populates="user")

