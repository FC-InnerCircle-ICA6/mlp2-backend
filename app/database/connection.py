from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# DATABASE_URL은 core/config.py에서 가져옴
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # connect_args={"check_same_thread": False} # SQLite 전용, PostgreSQL에는 필요 없음
)

# 세션 생성 (세션은 데이터베이스와 통신하는 실제 객체)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 모델의 베이스 클래스
Base = declarative_base()

# DB 세션 의존성 (FastAPI에서 사용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()