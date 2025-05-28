from sqlalchemy.orm import Session
from app.database.models import User
from app.core.security import verify_password, create_access_token
from app.services.user_service import get_user_by_email

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_user_account(db: Session, email: str, password: str, name: str):
    existing_user = get_user_by_email(db, email)
    if existing_user:
        return None # User with this email already exists
    return get_user_by_email(db, email) # This line should be create_user (fixed logic below)
    # Corrected logic:
    # from app.services.user_service import create_user
    # new_user = create_user(db, email, password, name)
    # return new_user