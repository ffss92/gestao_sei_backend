from api.utils.database import Base
from sqlalchemy import Column, Integer, Date, ForeignKey


class Vacation(Base):
  __tablename__ = "vacation"

  id = Column(Integer, primary_key=True)
  person_id = Column(Integer, ForeignKey("person.id", ondelete="CASCADE"), nullable=False)
  start_date = Column(Date, nullable=False)
  end_date = Column(Date, nullable=False)
