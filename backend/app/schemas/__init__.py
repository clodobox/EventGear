# backend/app/schemas/__init__.py
from app.schemas.equipment import (
    Equipment, 
    EquipmentCreate, 
    EquipmentUpdate,
    EquipmentWithRelations
)
from app.schemas.project import (
    Project,
    ProjectCreate,
    ProjectUpdate,
    ProjectEquipmentAdd
)
from app.schemas.contact import (
    Contact,
    ContactCreate,
    ContactUpdate
)

__all__ = [
    "Equipment", "EquipmentCreate", "EquipmentUpdate", "EquipmentWithRelations",
    "Project", "ProjectCreate", "ProjectUpdate", "ProjectEquipmentAdd",
    "Contact", "ContactCreate", "ContactUpdate"
]
