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
