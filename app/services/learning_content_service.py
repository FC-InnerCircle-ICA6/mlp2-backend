# certgo-backend/app/services/learning_content_service.py

from sqlalchemy.orm import Session, joinedload
from app.database import models
from typing import List, Optional
from uuid import UUID

def get_learning_content(db: Session, content_id: UUID):
    # 콘텐츠와 해당 섹션을 함께 로드하도록 joinedload 사용
    return db.query(models.LearningContent).options(joinedload(models.LearningContent.sections)).filter(models.LearningContent.id == content_id).first()

def get_learning_contents_by_certificate(db: Session, certificate_id: UUID, skip: int = 0, limit: int = 100) -> List[models.LearningContent]:
    return db.query(models.LearningContent).filter(models.LearningContent.certificate_id == certificate_id).offset(skip).limit(limit).all()

def get_all_learning_contents(db: Session, skip: int = 0, limit: int = 100) -> List[models.LearningContent]:
    return db.query(models.LearningContent).offset(skip).limit(limit).all()

def create_learning_content(
    db: Session,
    certificate_id: Optional[UUID],
    title: str,
    source_url: str,
    description: Optional[str],
    type: str,
    duration_minutes: Optional[int]
):
    db_content = models.LearningContent(
        certificate_id=certificate_id,
        title=title,
        source_url=source_url,
        description=description,
        type=type,
        duration_minutes=duration_minutes,
        processing_status="PENDING" # 초기 상태는 PENDING
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

def update_content_processing_status(db: Session, content_id: UUID, status: str, raw_text: Optional[str] = None):
    db_content = db.query(models.LearningContent).filter(models.LearningContent.id == content_id).first()
    if db_content:
        db_content.processing_status = status
        if raw_text:
            db_content.raw_text_content = raw_text
        db.commit()
        db.refresh(db_content)
    return db_content