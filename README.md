
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

docker network create certgo-network

docker compose up --build -d

초기 데이터 베이스 설정
docker compose exec certgo-backend alembic revision --autogenerate -m "Initial schema creation with comments for all tables"

docker compose exec certgo-backend alembic upgrade head


1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd certgo-backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Linux/macOS
    # venv\Scripts\activate # On Windows
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
