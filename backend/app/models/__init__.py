# backend/app/models/__init__.py
from app.models.base import BaseModel
from app.models.equipment import Equipment, Category, StorageLocation, EquipmentState
from app.models.project import Project, ProjectEquipment
from app.models.contact import Contact

__all__ = [
    "BaseModel",
    "Equipment", 
    "Category", 
    "StorageLocation", 
    "EquipmentState",
    "Project", 
    "ProjectEquipment",
    "Contact"
]
