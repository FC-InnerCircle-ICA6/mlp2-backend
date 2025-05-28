from celery import Celery
from app.core.config import settings

# Redis URL을 Celery 브로커 URL로 사용
celery_app = Celery(
    "certgo_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.content_processing_tasks"] # 처리할 태스크 모듈 지정
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Asia/Seoul', # 한국 시간대 설정
    enable_utc=True,
    broker_connection_retry_on_startup=True # Docker Compose 환경에서 Redis 먼저 시작 안 되어도 재시도
)