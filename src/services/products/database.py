# src/services/products/database.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

# 1. Define the path to the project's root directory
# 1 step back, the name of folder, preview, the service folder, preview, src folder
# a preview the main project folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# 2. Define the path to the database file
DB_FILE = PROJECT_ROOT / "omega_products.sqlite"

# 3. Create the database URL using the absolute path
DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False})

# enforces to use the orm relationships
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
