# backend/app/models/project.py
from sqlalchemy import Column, String, DateTime, Text, JSON, Date, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Project(Base):
    __tablename__ = "events"
    
    id = Column(String, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    client_name = Column(String(200))
    location = Column(String(500))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    setup_date = Column(DateTime(timezone=True))
    teardown_date = Column(DateTime(timezone=True))
    status = Column(String(50), default='planned')
    notes = Column(Text)
    extra_data = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    equipment_allocations = relationship("ProjectEquipment", back_populates="project")

class ProjectEquipment(Base):
    __tablename__ = "equipment_allocations"
    
    id = Column(String, primary_key=True)
    event_id = Column(String, ForeignKey("events.id"), nullable=False)
    equipment_id = Column(String, ForeignKey("equipment.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    notes = Column(Text)
    allocated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    project = relationship("Project", back_populates="equipment_allocations")
