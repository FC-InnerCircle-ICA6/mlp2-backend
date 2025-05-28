# certgo-backend/app/api/v1/learning_content/endpoints.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.api.v1.certificates import schemas as certificate_schemas # 자격증 스키마 재사용
from app.api.v1.learning_content import schemas
from app.services import learning_content_service
from app.core.dependencies import get_db, get_current_user # 인증 필요한 경우 get_current_user 사용

router = APIRouter()

@router.post("/", response_model=schemas.LearningContentResponse, status_code=status.HTTP_201_CREATED, summary="Create new Learning Content")
def create_learning_content(
    content_in: schemas.LearningContentBase,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # 콘텐츠 생성은 로그인 사용자만 가능
):
    """
    새로운 학습 콘텐츠를 생성합니다. (초기에는 PENDING 상태로 생성)
    """
    db_content = learning_content_service.create_learning_content(
        db,
        certificate_id=content_in.certificate_id, # 이 부분은 LearningContentBase에 포함되어야 함 (아래 스키마 수정 필요)
        title=content_in.title,
        source_url=content_in.source_url,
        description=content_in.description,
        type=content_in.type,
        duration_minutes=content_in.duration_minutes
    )
    # TODO: Celery task를 이용해 content_processing_tasks.process_content_task.delay(db_content.id) 호출
    return db_content


@router.get("/", response_model=List[schemas.LearningContentResponse], summary="Get Learning Content All")
def get_learning_content_all(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    전체 학습 콘텐츠 정보를 조회합니다. (섹션 정보도 포함)
    """
    content = learning_content_service.get_all_learning_contents(db)
    if content is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning Content not found")
    return content


@router.get("/{content_id}", response_model=schemas.LearningContentResponse, summary="Get Learning Content by ID")
def get_learning_content_by_id(
    content_id: UUID,
    db: Session = Depends(get_db)
):
    """
    특정 ID의 학습 콘텐츠 정보를 조회합니다. (섹션 정보도 포함)
    """
    content = learning_content_service.get_learning_content(db, content_id)
    if content is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning Content not found")
    return content

@router.get("/{content_id}/sections", response_model=List[schemas.ContentSectionResponse], summary="Get Sections for Learning Content")
def get_content_sections(
    content_id: UUID,
    db: Session = Depends(get_db)
):
    """
    특정 학습 콘텐츠의 모든 섹션(타임라인, 트랜스크립트 등)을 조회합니다.
    """
    content = learning_content_service.get_learning_content(db, content_id) # 다시 콘텐츠를 가져와서 섹션에 접근
    if content is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning Content not found")
    return content.sections # LearningContent 모델에 sections 관계가 정의되어 있어야 함