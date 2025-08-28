from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class ProjectBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    client_id: Optional[UUID] = None
    manager_id: Optional[UUID] = None
    start_date: datetime
    end_date: datetime
    prep_date: Optional[datetime] = None
    return_date: Optional[datetime] = None
    venue_name: Optional[str] = None
    venue_address: Optional[str] = None
    status: str = 'draft'
    notes: Optional[str] = None
    internal_notes: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class Project(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime]
    active: bool

class ProjectEquipmentAdd(BaseModel):
    equipment_id: UUID
    quantity_planned: int = 1
