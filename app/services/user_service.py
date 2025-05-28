from sqlalchemy.orm import Session
from app.database.models import User
from app.core.security import get_password_hash # 비밀번호 해싱 import

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str, name: str):
    hashed_password = get_password_hash(password)
    db_user = User(email=email, password_hash=hashed_password, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_profile(db: Session, user: User, name: str = None, bio: str = None, language: str = None, theme: str = None):
    if name is not None:
        user.name = name
    if bio is not None:
        user.bio = bio
    if language is not None:
        user.language = language
    if theme is not None:
        user.theme = theme
    db.commit()
    db.refresh(user)
    return user

def update_user_notifications(db: Session, user: User, email_notifications: bool = None, push_notifications: bool = None, marketing_emails: bool = None):
    if email_notifications is not None:
        user.email_notifications = email_notifications
    if push_notifications is not None:
        user.push_notifications = push_notifications
    if marketing_emails is not None:
        user.marketing_emails = marketing_emails
    db.commit()
    db.refresh(user)
    return user

def update_user_password(db: Session, user: User, new_password: str):
    user.password_hash = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}