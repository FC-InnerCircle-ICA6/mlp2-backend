from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.database import models # models.py에서 Base와 engine을 가져오기 위함

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0", # API 버전 추가 (선택 사항)
    description="CertGo Backend API documentation for learning and certification management.", # API 설명 추가 (선택 사항)
    openapi_url=f"{settings.API_V1_STR}/openapi.json", # OpenAPI JSON 스키마 경로
    docs_url="/docs", # Swagger UI 문서 경로
    redoc_url="/redoc", # ReDoc 문서 경로
)

# CORS 미들웨어 추가
# 프로덕션에서는 실제 프론트엔드 도메인만 허용하도록 설정
origins = [
    "http://localhost",
    "http://localhost:3000", # Next.js 프론트엔드 URL
    # 실제 배포 도메인 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 포함
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to CertGo Backend API!"}

# 데이터베이스 테이블 생성 (개발용. 프로덕션에서는 Alembic 같은 마이그레이션 도구 사용 권장)
@app.on_event("startup")
async def startup_event():
    # Alembic이 마이그레이션을 처리하므로 여기서는 Base.metadata.create_all()을 제거합니다.
    # alembic upgrade head 명령어가 Docker Compose command에 포함되어 있습니다.
    print("FastAPI application started. Alembic migrations are handled by Docker Compose entrypoint.")