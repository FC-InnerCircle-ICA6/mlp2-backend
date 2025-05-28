# certgo-backend/app/services/certificate_service.py

from sqlalchemy.orm import Session
from app.database import models
from typing import List, Optional
from uuid import UUID

def get_certificate(db: Session, certificate_id: UUID):
    return db.query(models.Certificate).filter(models.Certificate.id == certificate_id).first()

def get_certificates(db: Session, skip: int = 0, limit: int = 100) -> List[models.Certificate]:
    return db.query(models.Certificate).offset(skip).limit(limit).all()

def create_certificate(db: Session, name: str, description: Optional[str] = None, difficulty_level: Optional[int] = None, category: Optional[str] = None, is_premium: bool = False):
    db_certificate = models.Certificate(
        name=name,
        description=description,
        difficulty_level=difficulty_level,
        category=category,
        is_premium=is_premium
    )
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate