#!/bin/bash

# User Service - Structure Setup Script
# Run: chmod +x setup_user_service.sh && ./setup_user_service.sh

set -e

echo "🚀 Creating User Service structure..."

# Root directory
mkdir -p user-service
cd user-service

# Domain layer
mkdir -p app/domain/entities
mkdir -p app/domain/repositories

# Application layer
mkdir -p app/application/use_cases
mkdir -p app/application/dtos

# Infrastructure layer
mkdir -p app/infrastructure/database
mkdir -p app/infrastructure/messaging

# Presentation layer
mkdir -p app/presentation/routes

# Core
mkdir -p app/core

# Tests
mkdir -p tests/unit
mkdir -p tests/integration

# Create __init__.py files
touch app/__init__.py
touch app/domain/__init__.py
touch app/domain/entities/__init__.py
touch app/domain/repositories/__init__.py
touch app/application/__init__.py
touch app/application/use_cases/__init__.py
touch app/application/dtos/__init__.py
touch app/infrastructure/__init__.py
touch app/infrastructure/database/__init__.py
touch app/infrastructure/messaging/__init__.py
touch app/presentation/__init__.py
touch app/presentation/routes/__init__.py
touch app/core/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py

# Create main files
touch app/main.py
touch app/core/config.py
touch app/domain/entities/user.py
touch app/domain/repositories/user_repository.py
touch app/application/dtos/user_dto.py
touch app/application/use_cases/create_user_use_case.py
touch app/infrastructure/database/database.py
touch app/infrastructure/database/models.py
touch app/infrastructure/database/user_repository_impl.py
touch app/infrastructure/messaging/rabbitmq_publisher.py
touch app/presentation/routes/user_routes.py
touch app/presentation/dependencies.py

# Create test files
touch tests/unit/test_user_entity.py
touch tests/unit/test_create_user_use_case.py
touch tests/integration/test_user_routes.py
touch tests/conftest.py

# Create config files
touch .env
touch .env.example
touch requirements.txt
touch Dockerfile
touch .dockerignore
touch pytest.ini
touch README.md

# Create .env.example
cat > .env.example << 'EOF'
DATABASE_URL=postgresql+asyncpg://admin:admin123@localhost:5433/users_db
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=admin
RABBITMQ_PASS=admin123
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
DEBUG=True
EOF

# Create .dockerignore
cat > .dockerignore << 'EOF'
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
.pytest_cache
.coverage
htmlcov/
.env
.git
.gitignore
*.md
tests/
EOF

# Create pytest.ini
cat > pytest.ini << 'EOF'
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
addopts = 
    --verbose
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=70
EOF

# Create README.md
cat > README.md << 'EOF'
# User Service

Microservicio de gestión de usuarios con Clean Architecture + DDD.

## Estructura
```
user-service/
├── app/
│   ├── domain/          # Entities, repositories (interfaces)
│   ├── application/     # Use cases, DTOs
│   ├── infrastructure/  # DB, messaging, external services
│   ├── presentation/    # API routes, dependencies
│   └── core/           # Config, settings
├── tests/
│   ├── unit/
│   └── integration/
└── requirements.txt
```

## Setup

### Local
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

### Docker
```bash
docker-compose up -d postgres-user rabbitmq
docker-compose up user-service
```

## Tests
```bash
pytest --cov=app tests/ -v
```

## Endpoints
- `POST /users` - Create user (admin only)
- `GET /users` - List users
- `GET /users/{id}` - Get user by ID
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user
- `GET /health` - Health check

## Environment Variables
Copy `.env.example` to `.env` and configure:
- `DATABASE_URL`
- `RABBITMQ_HOST`
- `JWT_SECRET`
EOF

echo "✅ User Service structure created!"
echo ""
echo "📁 Directory structure:"
tree -L 4 -I '__pycache__|*.pyc' || find . -type d -not -path '*/\.*' | sed 's|[^/]*/|  |g'
echo ""
echo "🎯 Next steps:"
echo "1. cd user-service"
echo "2. Copy code from artifacts to respective files"
echo "3. python -m venv venv && source venv/bin/activate"
echo "4. pip install -r requirements.txt"
echo "5. uvicorn app.main:app --reload --port 8002"
