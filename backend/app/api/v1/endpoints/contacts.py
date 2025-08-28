from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.models.contact import Contact
from app.schemas.contact import Contact as ContactSchema, ContactCreate, ContactUpdate

router = APIRouter()

@router.get("/", response_model=List[ContactSchema])
def read_contacts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    contact_type: Optional[str] = None
):
    query = db.query(Contact).filter(Contact.active == True)
    
    if contact_type:
        query = query.filter(Contact.contact_type == contact_type)
    
    contacts = query.offset(skip).limit(limit).all()
    return contacts

@router.post("/", response_model=ContactSchema)
def create_contact(
    contact_in: ContactCreate,
    db: Session = Depends(get_db)
):
    db_contact = Contact(**contact_in.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
