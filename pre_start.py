from api.utils import init_db
from api.utils.database import SessionLocal

def init() -> None:
  db = SessionLocal()
  init_db(db)

def main() -> None:
  init()

if __name__ == "__main__":
  main()