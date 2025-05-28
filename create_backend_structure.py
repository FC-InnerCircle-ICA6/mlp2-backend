import os

def create_directory_and_files(base_path, structure):
    """
    주어진 구조에 따라 디렉토리와 파일을 생성합니다.
    빈 파일은 'file_name.py' 형태로, __init__.py는 'dir_name/__init__.py' 형태로 지정합니다.
    """
    for item in structure:
        if isinstance(item, str):
            # 파일인 경우
            file_path = os.path.join(base_path, item)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                pass # 빈 파일 생성
            print(f"Created file: {file_path}")
        elif isinstance(item, dict):
            # 디렉토리인 경우
            for dir_name, contents in item.items():
                dir_path = os.path.join(base_path, dir_name)
                os.makedirs(dir_path, exist_ok=True)
                print(f"Created directory: {dir_path}")
                # __init__.py 파일 생성
                init_py_path = os.path.join(dir_path, '__init__.py')
                if not os.path.exists(init_py_path):
                    with open(init_py_path, 'w') as f:
                        pass
                    print(f"Created file: {init_py_path}")
                create_directory_and_files(dir_path, contents)

# 백엔드 폴더 구조 정의
backend_structure = [
    {"app": [
        {"api": [
            {"v1": [
                {"auth": ["endpoints.py", "schemas.py"]},
                {"users": ["endpoints.py", "schemas.py"]},
                {"certificates": ["endpoints.py", "schemas.py"]},
                {"learning_content": ["endpoints.py", "schemas.py"]},
                {"quizzes": ["endpoints.py", "schemas.py"]},
                {"analytics": ["endpoints.py", "schemas.py"]},
                {"subscriptions": ["endpoints.py", "schemas.py"]},
                "router.py"
            ]},
        ]},
        {"core": [
            "config.py",
            "security.py",
            "dependencies.py"
        ]},
        {"database": [
            "connection.py",
            "models.py"
        ]},
        {"services": [
            "auth_service.py",
            "user_service.py",
            "content_service.py",
            "quiz_service.py",
            "analytics_service.py",
            "subscription_service.py",
            "ai_integration_service.py"
        ]},
        {"tasks": [
            "celery_worker.py",
            "content_processing_tasks.py"
        ]},
        "main.py"
    ]},
    {"tests": [
        {"api": [
            {"v1": [
                "test_auth.py",
                "test_users.py"
            ]},
        ]},
        "conftest.py"
    ]},
    {"scripts": [
        "init_db.py",
        "seed_data.py",
        "run_worker.sh"
    ]},
    ".env.example",
    ".gitignore",
    "Dockerfile",
    "requirements.txt",
    "README.md"
]

if __name__ == "__main__":
    base_dir = os.getcwd() # 현재 스크립트가 실행되는 디렉토리를 기준으로 생성
    print(f"Creating backend structure in: {base_dir}")
    create_directory_and_files(base_dir, backend_structure)
    print("\nBackend structure created successfully!")

    # .gitignore 파일에 추가할 내용 (이미 생성된 파일에 추가)
    gitignore_content = """
# Python virtual environment
/venv

# Environment variables
.env

# Pytest cache
.pytest_cache/
__pycache__/
*.pyc

# Docker
.dockerignore
.vscode/

# Qdrant client cache
.qdrant_cache/

# Celery
celerybeat.pid
celeryd.pid
*.log

# FastAPI docs
/docs/
"""
    with open(os.path.join(base_dir, '.gitignore'), 'a') as f:
        f.write(gitignore_content)
    print("Appended .gitignore content.")

    # requirements.txt에 기본 패키지 추가 (예시)
    requirements_content = """
fastapi==0.111.0
uvicorn==0.30.1
SQLAlchemy==2.0.30
psycopg2-binary==2.9.9
passlib==1.7.4
python-jose==3.3.0
python-multipart==0.0.9
pydantic==2.7.4
pydantic-settings==2.3.3
qdrant-client==1.9.0
redis==5.0.4
celery==5.4.0
# AI/ML 관련 라이브러리 (필요에 따라 추가)
# transformers
# torch
# openai
# huggingface_hub
# youtube-dlp (for video processing)
# beautifulsoup4 (for web scraping)
"""
    with open(os.path.join(base_dir, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)
    print("Populated requirements.txt with basic packages.")

    # Dockerfile 기본 내용 추가 (예시)
    dockerfile_content = """
# Python 버전 지정 (Node.js 버전과 무관)
FROM python:3.10-slim-buster

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FastAPI 애플리케이션 실행 명령어
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# 또는 gunicorn과 함께 사용 (프로덕션 권장)
CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

EXPOSE 8000
"""
    with open(os.path.join(base_dir, 'Dockerfile'), 'w') as f:
        f.write(dockerfile_content)
    print("Populated Dockerfile with basic content.")

    # README.md 기본 내용 추가
    readme_content = """
# CertGo Backend

This is the backend service for CertGo, built with Python (FastAPI), PostgreSQL, Redis, and Qdrant. It handles user management, learning content processing (including AI features), quiz generation, analytics, and subscription management.

## Project Structure

The project follows a modular structure for better organization and scalability.

## Setup

### Prerequisites

* Python 3.9+
* PostgreSQL
* Redis
* Qdrant
* fnm (for Node.js frontend)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd certgo-backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Linux/macOS
    # venv\\Scripts\\activate # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**
    Create a `.env` file in the root directory based on `.env.example`.

    ```env
    # .env example
    DATABASE_URL="postgresql://user:password@host:port/dbname"
    REDIS_URL="redis://localhost:6379/0"
    QDRANT_HOST="localhost:6333"
    JWT_SECRET_KEY="your_jwt_secret_key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    # Add any AI API keys here, e.g., OPENAI_API_KEY, HUGGINGFACE_API_KEY
    AI_API_KEY="your_ai_api_key"
    ```

5.  **Database Setup:**
    Ensure your PostgreSQL database is running.
    Run the database initialization script:
    ```bash
    python scripts/init_db.py
    ```
    (You will need to implement the content of `init_db.py` to apply the SQL schema.)

### Running the Application

1.  **Start the FastAPI server:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The API documentation will be available at `http://127.0.0.1:8000/docs` (Swagger UI) or `http://127.0.0.1:8000/redoc`.

2.  **Start the Celery worker (in a separate terminal):**
    Ensure Redis is running as the message broker.
    ```bash
    celery -A app.tasks.celery_worker worker -l info
    ```

## Development

* **Tests:** Run tests using `pytest`.
    ```bash
    pytest tests/
    ```

## Deployment

Refer to the `Dockerfile` for containerization. This application can be deployed on various cloud platforms (e.g., AWS ECS/EKS, Google Cloud Run, Azure App Service).

## Contributing

Feel free to contribute to the project.
"""
    with open(os.path.join(base_dir, 'README.md'), 'w') as f:
        f.write(readme_content)
    print("Populated README.md with basic content.")