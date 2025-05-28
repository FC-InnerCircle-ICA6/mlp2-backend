# certgo-backend/app/api/v1/certificates/endpoints.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.api.v1.certificates import schemas
from app.services import certificate_service, learning_content_service
from app.core.dependencies import get_db, get_current_user # 인증 필요한 경우 get_current_user 사용

router = APIRouter()

@router.post("/", response_model=schemas.CertificateResponse, status_code=status.HTTP_201_CREATED, summary="Create a new Certificate")
def create_certificate(
    certificate_in: schemas.CertificateBase,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # 관리자 권한 필요 시, Role-based access control (RBAC) 추가 필요
):
    """
    새로운 자격증 정보를 생성합니다.
    """
    db_certificate = certificate_service.create_certificate(
        db,
        name=certificate_in.name,
        description=certificate_in.description,
        difficulty_level=certificate_in.difficulty_level,
        category=certificate_in.category,
        is_premium=certificate_in.is_premium
    )
    return db_certificate

@router.get("/", response_model=List[schemas.CertificateResponse], summary="Get all Certificates")
def get_all_certificates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    모든 자격증 목록을 조회합니다.
    """
    certificates = certificate_service.get_certificates(db, skip=skip, limit=limit)
    return certificates

@router.get("/{certificate_id}", response_model=schemas.CertificateResponse, summary="Get Certificate by ID")
def get_certificate_by_id(
    certificate_id: UUID,
    db: Session = Depends(get_db)
):
    """
    특정 ID의 자격증 정보를 조회합니다.
    """
    certificate = certificate_service.get_certificate(db, certificate_id)
    if certificate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")
    return certificate

@router.get("/{certificate_id}/contents", response_model=List[schemas.LearningContentResponse], summary="Get Learning Contents by Certificate ID")
def get_contents_by_certificate(
    certificate_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    특정 자격증에 속하는 학습 콘텐츠 목록을 조회합니다.
    """
    contents = learning_content_service.get_learning_contents_by_certificate(db, certificate_id, skip=skip, limit=limit)
    return contents