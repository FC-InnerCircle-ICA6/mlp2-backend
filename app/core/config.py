from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "CertGo Backend"
    API_V1_STR: str = "/api/v1" # Traefik 라우팅과 일치하도록 /api/v1로 변경
    DATABASE_URL: str
    REDIS_URL: str
    QDRANT_HOST: str
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24시간

    # AI 관련 설정
    AI_API_KEY: str = "" # AI_API_KEY 설정 (필요시)
    QDRANT_API_KEY: str = "" # Qdrant API Key (클라우드 Qdrant 사용 시)

    # pydantic-settings가 .env 파일을 로드하도록 설정
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()