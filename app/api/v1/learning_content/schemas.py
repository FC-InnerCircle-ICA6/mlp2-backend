# certgo-backend/app/api/v1/learning_content/schemas.py

from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

# LearningContentBase (certificates 스키마에서 가져온 것을 로컬에서 확장)
class LearningContentBase(BaseModel):
    certificate_id: Optional[UUID] = None # 콘텐츠 생성 시 자격증 ID 연결
    title: str
    source_url: str
    description: Optional[str] = None
    type: str # 'video', 'document', 'text', 'quiz_set'
    duration_minutes: Optional[int] = None

class LearningContentResponse(LearningContentBase):
    id: UUID
    processing_status: str
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