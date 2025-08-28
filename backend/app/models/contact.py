# backend/app/models/contact.py
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.db.base_class import Base

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(String, primary_key=True)
    code = Column(String(50), unique=True)
    company_name = Column(String(200))
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    contact_type = Column(String(50))  # 'client', 'supplier', 'technician', 'other'
    notes = Column(Text)
    active = Column(Boolean, default=True)
    extra_data = Column(JSON, default={})  # Renommé de metadata à extra_data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
