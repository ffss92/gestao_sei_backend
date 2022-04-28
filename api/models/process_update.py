from api.utils.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime


class ProcessUpdate(Base):
  __tablename__ = "process_update"

  id = Column(Integer, primary_key=True)
  description = Column(String(255), nullable=False)
  user_id = Column(Integer, ForeignKey("user.id"), onupdate="CASCADE")
  process_id = Column(Integer, ForeignKey("process.id", ondelete="CASCADE"))
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
  
  user = relationship("User", back_populates="process_updates")
  process = relationship("Process", back_populates="updates")