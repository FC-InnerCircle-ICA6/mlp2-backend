from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import sys # 이 줄을 추가합니다.
import os


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    

# --- 추가 시작 ---

# 1. 프로젝트 루트 디렉토리를 sys.path에 추가
# 이렇게 해야 Alembic이 'app' 모듈을 올바르게 임포트할 수 있습니다.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2. .env 파일 로드
# Alembic이 데이터베이스 URL 등의 환경 변수를 읽을 수 있도록 합니다.
from dotenv import load_dotenv
load_dotenv()

# 3. FastAPI 프로젝트의 설정 및 모델 임포트
# settings 객체를 통해 DATABASE_URL에 접근
from app.core.config import settings
# SQLAlchemy Base 메타데이터를 임포트
from app.database.connection import Base
# 모든 SQLAlchemy 모델을 임포트 (Base.metadata에 등록되도록 함)
# 만약 모든 모델이 특정 파일에서 import 된다면, 해당 파일만 import 해도 됩니다.
# 여기서는 예시로 모든 모델 파일을 명시적으로 임포트합니다.
from app.database.models import (
    User, Certificate, LearningContent, ContentSection, Quiz,
    UserQuizAttempt, UserAnswer, UserLearningProgress,
    SubscriptionPlan, UserSubscription, LoginHistory
)

# --- 추가 끝 ---

# 이 부분은 Alembic이 DB 스키마를 비교할 때 사용할 메타데이터입니다.
# app.database.models에서 임포트한 Base의 metadata를 지정합니다.
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # settings.DATABASE_URL을 사용하여 데이터베이스 엔진을 생성합니다.
    connectable = engine_from_config(
        {"sqlalchemy.url": settings.DATABASE_URL}, # .env에서 로드된 URL 사용
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            dialect_opts={"paramstyle": "named"},
            # COMMENT ON 문을 마이그레이션에 포함하려면 include_object를 사용합니다.
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()

# COMMENT ON 문을 포함하기 위한 헬퍼 함수
def include_object(object, name, type_, reflected, comparable_objects):
    """
    이 함수는 Alembic이 데이터베이스 스키마와 ORM 모델을 비교할 때,
    어떤 객체(테이블, 컬럼)를 마이그레이션 스크립트에 포함할지 결정합니다.
    특히, SQLAlchemy 모델에 'comment' 인자가 정의된 경우,
    해당 주석이 DDL (Data Definition Language)에 포함되도록 합니다.
    """
    # 테이블에 comment가 있는 경우 포함
    if type_ == "table" and hasattr(object, 'comment') and object.comment:
        return True
    # 컬럼에 comment가 있는 경우 포함
    if type_ == "column" and hasattr(object, 'comment') and object.comment:
        return True
    # 그 외의 모든 객체(예: 제약 조건, 인덱스)는 기본적으로 포함
    return True

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
