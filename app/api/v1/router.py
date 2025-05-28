from fastapi import APIRouter

from app.api.v1.auth.endpoints import router as auth_router
from app.api.v1.users.endpoints import router as user_router
# 다른 도메인의 라우터도 여기에 임포트하고 include_router로 추가

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
# api_router.include_router(certificates_router, prefix="/certificates", tags=["certificates"])
# api_router.include_router(learning_content_router, prefix="/learning-content", tags=["learning-content"])
# api_router.include_router(quizzes_router, prefix="/quizzes", tags=["quizzes"])
# api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
# api_router.include_router(subscriptions_router, prefix="/subscriptions", tags=["subscriptions"])