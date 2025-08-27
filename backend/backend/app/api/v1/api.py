from fastapi import APIRouter

from app.api.v1.endpoints import equipment, projects, contacts

api_router = APIRouter()

api_router.include_router(equipment.router, prefix="/equipment", tags=["equipment"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
