# backend/app/models/equipment.py
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Equipment(Base):
    __tablename__ = "equipment"
    
    id = Column(String, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    quantity_total = Column(Integer, default=1)
    quantity_available = Column(Integer, default=1)
    location = Column(String(200))
    purchase_date = Column(DateTime)
    purchase_price = Column(Float)
    rental_price_daily = Column(Float)
    weight_kg = Column(Float)
    dimensions = Column(String(100))
    notes = Column(Text)
    active = Column(Boolean, default=True)
    extra_data = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    project_allocations = relationship("ProjectEquipment", backref="equipment")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(String, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    parent_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class StorageLocation(Base):
    __tablename__ = "storage_locations"
    
    id = Column(String, primary_key=True)
    name = Column(String(200), nullable=False)
    address = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EquipmentState(Base):
    __tablename__ = "equipment_states"
    
    id = Column(String, primary_key=True)
    equipment_id = Column(String, nullable=False)
    state = Column(String(50))
    notes = Column(Text)
    checked_by = Column(String(100))
    checked_at = Column(DateTime(timezone=True), server_default=func.now())
