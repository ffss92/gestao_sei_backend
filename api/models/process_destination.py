from api.utils.database import Base
from sqlalchemy import Column, ForeignKey, Table


process_destination_rel = Table(
  "process_destination",
  Base.metadata,
  Column("process_id", ForeignKey("process.id")),
  Column("destination_id", ForeignKey("destination.id"))
)