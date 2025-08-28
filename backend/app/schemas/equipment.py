from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import date, datetime
from uuid import UUID

class EquipmentBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    storage_location_id: Optional[UUID] = None
    state_id: Optional[UUID] = None
    serial_number: Optional[str] = None
    barcode: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    quantity_total: int = 1
    unit_value: Optional[float] = None
    purchase_date: Optional[date] = None
    warranty_end_date: Optional[date] = None
    maintenance_interval_days: Optional[int] = None
    specifications: Optional[Dict[str, Any]] = {}
    metadata: Optional[Dict[str, Any]] = {}

class EquipmentCreate(EquipmentBase):
    pass

class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity_total: Optional[int] = None
    storage_location_id: Optional[UUID] = None
    state_id: Optional[UUID] = None

class Equipment(EquipmentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    quantity_available: int
    usage_count: int
    created_at: datetime
    updated_at: Optional[datetime]
    active: bool

class EquipmentWithRelations(Equipment):
    category: Optional[Dict] = None
    location: Optional[Dict] = None
    state: Optional[Dict] = None
