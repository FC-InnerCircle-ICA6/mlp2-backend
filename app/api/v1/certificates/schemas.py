# certgo-backend/app/api/v1/certificates/schemas.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class CertificateBase(BaseModel):
    name: str
    description: Optional[str] = None
    difficulty_level: Optional[int] = None
    category: Optional[str] = None
    is_premium: bool = False

class CertificateResponse(CertificateBase):
    id: UUID

    class Config:
        from_attributes = True # Pydantic v2: orm_mode = True for SQLAlchemy models

class LearningContentBase(BaseModel):
    title: str
    source_url: str
    description: Optional[str] = None
    type: str # 'video', 'document', 'text', 'quiz_set'
    duration_minutes: Optional[int] = None

class LearningContentResponse(LearningContentBase):
    id: UUID
    certificate_id: Optional[UUID] = None # Foreign Key
    processing_status: str # 'PENDING', 'PROCESSING', 'COMPLETED', 'FAILED'
    qdrant_collection_name: Optional[str] = None
    # raw_text_content는 응답에 포함하지 않음 (대용량)

    class Config:
        from_attributes = True

class ContentSectionResponse(BaseModel):
    id: UUID
    content_id: UUID
    section_title: Optional[str] = None
    section_text: str
    start_timestamp: Optional[str] = None
    end_timestamp: Optional[str] = None
    order_index: int

    class Config:
        from_attributes = True