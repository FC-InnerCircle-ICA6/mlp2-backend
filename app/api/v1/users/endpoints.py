from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.users import schemas
from app.database.models import User
from app.core.dependencies import get_db, get_current_user
from app.core.security import verify_password
from app.services import user_service

router = APIRouter()

@router.get("/me", response_model=schemas.UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.UserResponse)
def update_current_user_profile(
    user_update: schemas.UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_user = user_service.update_user_profile(
        db,
        user=current_user,
        name=user_update.name,
        bio=user_update.bio,
        language=user_update.language,
        theme=user_update.theme
    )
    return updated_user

@router.put("/me/notifications", response_model=schemas.UserResponse)
def update_current_user_notifications(
    notif_update: schemas.UserNotificationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_user = user_service.update_user_notifications(
        db,
        user=current_user,
        email_notifications=notif_update.email_notifications,
        push_notifications=notif_update.push_notifications,
        marketing_emails=notif_update.marketing_emails
    )
    return updated_user

@router.put("/me/password", response_model=schemas.MessageResponse)
def update_current_user_password(
    password_update: schemas.UserPasswordUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(password_update.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    if password_update.new_password != password_update.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirmation do not match"
        )
    user_service.update_user_password(db, current_user, password_update.new_password)
    return {"message": "Password updated successfully"}

@router.delete("/me", response_model=schemas.MessageResponse)
def delete_current_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 실제 계정 삭제 로직 (확인 메일 발송 등 추가 필요)
    user_service.delete_user(db, current_user)
    return {"message": "Account deletion request received. Please check your email."}

# Login history (requires LoginHistory model and service)
# @router.get("/me/login-history", response_model=List[schemas.LoginHistoryResponse])
# def read_user_login_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     history = user_service.get_user_login_history(db, current_user.id)
#     return history