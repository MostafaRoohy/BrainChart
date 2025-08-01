# This file configures the connection to the SQLite database using SQLAlchemy,
# creating the necessary engine and session management tools for the backend to use.
###################################################################################################
###################################################################################################
###################################################################################################
#
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
#
###################################################################################################
###################################################################################################
###################################################################################################
#
BASE_DIR = Path(__file__).resolve().parent
DB_DIR  = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)
DB_FILE = DB_DIR / "tradingview.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

engine       = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():

    db = SessionLocal()

    try:

        yield db
    #
    finally:

        db.close()
    #
#
###################################################################################################
###################################################################################################
###################################################################################################
#