from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date, datetime

from app.database import get_db
from app.models.project import Project, ProjectEquipment
from app.models.equipment import Equipment
from app.schemas.project import (
    Project as ProjectSchema,
    ProjectCreate,
    ProjectUpdate,
    ProjectEquipmentAdd
)

router = APIRouter()

@router.get("/", response_model=List[ProjectSchema])
def read_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
):
    query = db.query(Project)
    
    if status:
        query = query.filter(Project.status == status)
    
    projects = query.offset(skip).limit(limit).all()
    return projects

@router.post("/", response_model=ProjectSchema)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db)
):
    if db.query(Project).filter(Project.code == project_in.code).first():
        raise HTTPException(status_code=400, detail="Code already exists")
    
    db_project = Project(**project_in.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.post("/{project_id}/equipment")
def add_equipment_to_project(
    project_id: UUID,
    equipment: ProjectEquipmentAdd,
    db: Session = Depends(get_db)
):
    # Vérifier que le projet existe
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Vérifier que l'équipement existe
    equip = db.query(Equipment).filter(Equipment.id == equipment.equipment_id).first()
    if not equip:
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    # Vérifier la disponibilité
    if equip.quantity_available < equipment.quantity_planned:
        raise HTTPException(
            status_code=400, 
            detail=f"Not enough equipment available. Available: {equip.quantity_available}"
        )
    
    # Ajouter l'équipement au projet
    project_equipment = ProjectEquipment(
        project_id=project_id,
        equipment_id=equipment.equipment_id,
        quantity_planned=equipment.quantity_planned
    )
    
    # Mettre à jour la quantité disponible
    equip.quantity_available -= equipment.quantity_planned
    
    db.add(project_equipment)
    db.commit()
    
    return {"message": "Equipment added to project"}

@router.post("/{project_id}/checkout")
def checkout_equipment(
    project_id: UUID,
    db: Session = Depends(get_db)
):
    """Marquer le matériel comme sorti pour le projet"""
    project_equipment = db.query(ProjectEquipment).filter(
        ProjectEquipment.project_id == project_id
    ).all()
    
    for pe in project_equipment:
        pe.checkout_date = datetime.now()
        pe.quantity_prepared = pe.quantity_planned
    
    project = db.query(Project).filter(Project.id == project_id).first()
    project.status = 'ongoing'
    
    db.commit()
    return {"message": "Equipment checked out"}
