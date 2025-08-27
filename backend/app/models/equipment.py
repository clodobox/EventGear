from sqlalchemy import Column, String, Integer, Numeric, Text, Date, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import BaseModel

class Equipment(Base, BaseModel):
    __tablename__ = "equipment"
    __table_args__ = {"schema": "eventgear"}
    
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Relations
    category_id = Column(UUID(as_uuid=True), ForeignKey("eventgear.categories.id"))
    storage_location_id = Column(UUID(as_uuid=True), ForeignKey("eventgear.storage_locations.id"))
    state_id = Column(UUID(as_uuid=True), ForeignKey("eventgear.equipment_states.id"))
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("eventgear.contacts.id"))
    
    # Identification
    serial_number = Column(String(200))
    barcode = Column(String(200), index=True)
    manufacturer = Column(String(200))
    model = Column(String(200))
    
    # Quantities
    quantity_total = Column(Integer, default=1)
    quantity_available = Column(Integer, default=1, index=True)
    unit_value = Column(Numeric(10, 2))
    currency = Column(String(3), default="EUR")
    
    # Dates
    purchase_date = Column(Date)
    warranty_end_date = Column(Date)
    last_maintenance_date = Column(Date)
    
    # Maintenance
    maintenance_interval_days = Column(Integer)
    usage_count = Column(Integer, default=0)
    
    # JSON fields for flexibility
    specifications = Column(JSON, default={})
    metadata = Column(JSON, default={})
    
    # Relations
    category = relationship("Category", back_populates="equipment")
    location = relationship("StorageLocation", back_populates="equipment")
    state = relationship("EquipmentState", back_populates="equipment")
    projects = relationship("ProjectEquipment", back_populates="equipment")
    history = relationship("EquipmentHistory", back_populates="equipment")

class Category(Base, BaseModel):
    __tablename__ = "categories"
    __table_args__ = {"schema": "eventgear"}
    
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("eventgear.categories.id"))
    color = Column(String(7))
    icon = Column(String(50))
    
    equipment = relationship("Equipment", back_populates="category")

class StorageLocation(Base, BaseModel):
    __tablename__ = "storage_locations"
    __table_args__ = {"schema": "eventgear"}
    
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    address = Column(Text)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("eventgear.storage_locations.id"))
    notes = Column(Text)
    
    equipment = relationship("Equipment", back_populates="location")

class EquipmentState(Base, BaseModel):
    __tablename__ = "equipment_states"
    __table_args__ = {"schema": "eventgear"}
    
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    color = Column(String(7))
    can_be_rented = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    
    equipment = relationship("Equipment", back_populates="state")
