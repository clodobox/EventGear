from typing import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

def get_db() -> Generator:
    """
    Générateur de session de base de données.
    Assure que la session est fermée après utilisation.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
