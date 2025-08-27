from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.api import deps
from app.database import get_db
from app.models.equipment import Equipment
from app.schemas.equipment import (
    Equipment as EquipmentSchema,
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentWithRelations
)

router = APIRouter()

@router.get("/", response_model=List[EquipmentSchema])
def read_equipment(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category_id: Optional[UUID] = None,
    available_only: bool = False
):
    """Liste du matériel avec filtres"""
    query = db.query(Equipment).filter(Equipment.active == True)
    
    if search:
        query = query.filter(
            Equipment.name.ilike(f"%{search}%") |
            Equipment.code.ilike(f"%{search}%") |
            Equipment.barcode == search
        )
    
    if category_id:
        query = query.filter(Equipment.category_id == category_id)
    
    if available_only:
        query = query.filter(Equipment.quantity_available > 0)
    
    equipment = query.offset(skip).limit(limit).all()
    return equipment

@router.post("/", response_model=EquipmentSchema)
def create_equipment(
    equipment_in: EquipmentCreate,
    db: Session = Depends(get_db)
):
    """Créer un nouvel équipement"""
    # Vérifier que le code est unique
    if db.query(Equipment).filter(Equipment.code == equipment_in.code).first():
        raise HTTPException(status_code=400, detail="Code already exists")
    
    db_equipment = Equipment(**equipment_in.dict())
    db_equipment.quantity_available = equipment_in.quantity_total
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment

@router.get("/{equipment_id}", response_model=EquipmentWithRelations)
def read_equipment_by_id(
    equipment_id: UUID,
    db: Session = Depends(get_db)
):
    """Détails d'un équipement"""
    equipment = db.query(Equipment).filter(
        Equipment.id == equipment_id,
        Equipment.active == True
    ).first()
    
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    return equipment

@router.patch("/{equipment_id}", response_model=EquipmentSchema)
def update_equipment(
    equipment_id: UUID,
    equipment_in: EquipmentUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour un équipement"""
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    update_data = equipment_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(equipment, field, value)
    
    db.commit()
    db.refresh(equipment)
    return equipment

@router.delete("/{equipment_id}")
def delete_equipment(
    equipment_id: UUID,
    db: Session = Depends(get_db)
):
    """Désactiver un équipement (soft delete)"""
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    equipment.active = False
    db.commit()
    return {"message": "Equipment deactivated"}

@router.get("/{equipment_id}/availability")
def check_availability(
    equipment_id: UUID,
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db)
):
    """Vérifier la disponibilité sur une période"""
    # Logique pour vérifier les conflits avec les projets
    # À implémenter avec la table project_equipment
    pass
