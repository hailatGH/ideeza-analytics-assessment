# IDEEZA - Senior Backend Developer Assessment

This project is a technical assessment for the **Senior Backend Developer** position at **IDEEZA**. It implements a high-performance Django-based analytics service designed to provide deep insights into blog platforms. 

The assessment showcases proficiency in:
- **Advanced Django ORM**: Complex aggregations, annotations, and time-series data handling.
- **System Architecture**: Multi-stage Dockerization, modular settings management, and automated service orchestration.
- **Code Quality & DevSecOps**: Linting, pre-commit hooks, and CI/CD via GitHub Actions.
- **API Design**: Flexible, JSON-based dynamic filtering and highly optimized endpoints.

## 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- **Docker & Docker Compose** (Recommended)
- **Python 3.13+** (If running locally)
- **Poetry** (Python package manager)

---

### 🐳 How to use Docker (Recommended)

The project is fully containerized using a multi-stage `Dockerfile` and `compose.yml`.

1.  **Clone the repository**:
    ```bash
    git clone git@github.com:hailatGH/ideeza-analytics-assessment.git
    cd ideeza-analytics-assessment
    ```

2.  **Environment Setup**:
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```

3.  **Start the services**:
    ```bash
    docker compose up --build
    ```
    This will:
    - Start a **PostgreSQL 17** database.
    - Run an **initialization service** that automatically applies migrations and seeds the database with demo data (if `DJANGO_ENV=development`).
    - Start the **Django development server** with hot-reloading.

4.  **Access the API**:
    The API will be available at `http://localhost:8000`.

---

### 💻 Local Installation (Manual)

If you prefer to run without Docker:

1.  **Install dependencies**:
    ```bash
    poetry install --no-root
    ```

2.  **Set up Database**:
    Ensure you have a PostgreSQL database running and update the `DATABASE_URL` in your `.env` file.

3.  **Run Migrations & Seed**:
    ```bash
    poetry run python manage.py migrate
    poetry run python manage.py seed_data
    ```

4.  **Start Server**:
    ```bash
    poetry run python manage.py runserver
    ```

---

## 🛠️ Tools Used

- **Framework**: [Django 6.0](https://www.djangoproject.com/) & [Django Rest Framework](https://www.django-rest-framework.org/)
- **Database**: [PostgreSQL 17](https://www.postgresql.org/)
- **State Management**: [Poetry](https://python-poetry.org/)
- **Production Server**: [Gunicorn](https://gunicorn.org/)
- **CI/CD**: [GitHub Actions](https://github.com/features/actions) (Linting via `pre-commit`)
- **Code Quality**: `black`, `isort`, `flake8`, `mypy`
- **Environment**: `python-dotenv` & `dj-database-url`

---

## 📊 API Showcase & Filtering

The service provides three main analytics endpoints. All endpoints support a powerful **JSON-based dynamic filter system**.

### Base URL: `/analytics/`

#### 1. Blog Views Analytics
`GET /analytics/blog-views/`
Groups views by user or country.
- **Params**: `object_type` (user|country), `filters` (JSON)

#### 2. Top Analytics
`GET /analytics/top/`
Returns the top 10 entities by view count.
- **Params**: `top` (blog|user|country), `filters` (JSON)

#### 3. Performance Analytics
`GET /analytics/performance/`
Provides time-series data for blogs and views.
- **Params**: `compare` (day|week|month|year), `user_id` (optional), `filters` (JSON)

### 🔍 Filtering Examples

You can pass complex filters via the `filters` query parameter:

*   **Simple Equality**:
    `?filters={"eq": {"author__username": "michael"}}`
*   **Greater Than / Range**:
    `?filters={"created_at__gt": "2024-01-01"}`
*   **Logical AND**:
    `?filters={"and": [{"eq": {"author__profile__country__code": "US"}}, {"created_at__gt": "2023-01-01"}]}`
*   **Logical OR**:
    `?filters={"or": [{"eq": {"author__username": "michael"}}, {"eq": {"author__username": "eva"}}]}`

---

## 🏗️ Project Architecture

- **Multi-Environment Settings**: Split into `common`, `dev`, `stg`, and `prd` under `core/settings/`. Controlled via `DJANGO_ENV`.
- **Initialization Service**: A dedicated Docker service (`init`) that handles database readiness, migrations, and idempotent seeding.
- **Production Ready**: The production Docker stage uses Gunicorn with multiple workers and optimized system headers.

---

## 🚀 Future Improvements

- [ ] **Testing**: Implement a comprehensive test suite using `pytest-django`.
    - Unit tests for `parse_dynamic_filters`.
    - Integration tests for analytics views.
- [ ] **Caching**: Integrate Redis for caching frequent analytics queries.
- [ ] **Swagger/OpenAPI**: Add `drf-spectacular` for interactive API documentation.
- [ ] **Asynchronous Tasks**: Use Celery for heavy data aggregation tasks if the dataset grows significantly.
- [ ] **Security**: Implement JWT authentication for analytics endpoints.

---

## 👨‍💻 Author

**Hailemichael Atrsaw (Michael)**
[hailemichael.atrsaw@gmail.com](mailto:hailemichael.atrsaw@gmail.com)
