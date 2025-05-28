import sys
import os
from sqlalchemy import create_engine
from app.database.connection import Base
from app.database.models import * # 모든 모델을 임포트하여 Base.metadata에 등록

# 환경 변수 로드를 위해 app.core.config 임포트
from app.core.config import settings

# DB URL은 settings에서 가져옴
DATABASE_URL = settings.DATABASE_URL

def init_db():
    print(f"Attempting to connect to database at: {DATABASE_URL}")
    try:
        engine = create_engine(DATABASE_URL)
        # 모든 테이블 생성 (이미 존재하면 건너뜀)
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully or already exist.")
    except Exception as e:
        print(f"Error connecting to database or creating tables: {e}")
        sys.exit(1) # 에러 발생 시 스크립트 종료

if __name__ == "__main__":
    # 스크립트 실행 전에 환경 변수가 로드되도록 (예: .env 파일)
    # 실제 Docker 환경에서는 Docker Compose가 환경 변수를 주입합니다.
    # 로컬에서 이 스크립트를 직접 실행할 때는 dotenv 등을 사용할 수 있습니다.
    # from dotenv import load_dotenv
    # load_dotenv()
    init_db()