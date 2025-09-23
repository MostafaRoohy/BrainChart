#
# This file configures the connection to the SQLite database using SQLAlchemy,
# creating the necessary engine and session management tools for the backend to use.
#
# Contains the SQLAlchemy (or other ORM) models.
# These define the actual database tables and their relationships.
# Think of this as the database-layer definition.
# Defines how your data is stored in the database (the database schema).
# This module defines the database table schemas using the SQLAlchemy ORM,
# specifying the structure for tables like charts and shapes.
#
###################################################################################################
###################################################################################################
###################################################################################################
#
from pathlib import Path
from datetime import datetime

from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base ?????????
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Index
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
#
###################################################################################################
###################################################################################################
###################################################################################################
#
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_DIR   = ROOT_DIR / "runtime" / "database"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_FILE  = DB_DIR / "BrainChart.db"
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
class Chart(Base):

    __tablename__ = "charts"
    
    id         = Column(Integer , primary_key=True, index=True)
    name       = Column(String  , default="New Chart")
    symbol     = Column(String  , unique=True, index=True) 
    created_at = Column(DateTime, default=datetime.now)
    timeframe  = Column(String)
    shapes     = relationship("Shape", back_populates="chart")
#


class Shape(Base):

    __tablename__  = "shapes"
    __table_args__ = (Index("ix_shapes_symbol_sig", "symbol", "sig"),)

    id         = Column(Integer , primary_key=True, index=True)
    symbol     = Column(String  , nullable=False  , index=True)
    shape_type = Column(String  , nullable=False)
    points     = Column(JSON    , nullable=False)
    options    = Column(JSON    , nullable=False , default=dict)
    sig        = Column(String  , nullable=False  , index=True)
    created_at = Column(DateTime, default=datetime.now)

    chart_id   = Column(Integer, ForeignKey("charts.id"), nullable=True)
    chart      = relationship("Chart", back_populates="shapes")
#
###################################################################################################
###################################################################################################
###################################################################################################
#