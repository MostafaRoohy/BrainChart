# Contains the SQLAlchemy (or other ORM) models.
# These define the actual database tables and their relationships.
# Think of this as the database-layer definition.
# Defines how your data is stored in the database (the database schema).
# This module defines the database table schemas using the SQLAlchemy ORM,
# specifying the structure for tables like charts and shapes.
###################################################################################################
###################################################################################################
###################################################################################################
#
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
#
###################################################################################################
###################################################################################################
###################################################################################################
#
Base = declarative_base()

class Chart(Base):

    __tablename__ = "charts"
    
    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String, default="New Chart")
    symbol     = Column(String, unique=True, index=True) 
    timeframe  = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    shapes     = relationship("Shape", back_populates="chart")
#

class Shape(Base):

    __tablename__ = "shapes"
    
    id         = Column(Integer, primary_key=True, index=True)
    chart_id   = Column(Integer, ForeignKey("charts.id"))
    shape_id   = Column(String, nullable=True)
    shape_type = Column(String)
    # shape_code = Column(Integer, unique=True, nullable=False)
    shape_code = Column(Integer, nullable=False)
    shape_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    chart = relationship("Chart", back_populates="shapes")
#
###################################################################################################
###################################################################################################
###################################################################################################
#

