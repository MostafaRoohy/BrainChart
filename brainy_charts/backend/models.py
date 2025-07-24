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
    symbol     = Column(String)
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
    shape_code = Column(Integer, unique=True, nullable=False)
    shape_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    chart = relationship("Chart", back_populates="shapes")
#
###################################################################################################
###################################################################################################
###################################################################################################
#