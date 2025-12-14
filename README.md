# Sistema Gestión Usuarios - Full-Stack IA

## Arquitectura
- 4 microservicios: Auth, User, Audit, AI
- Frontend React + TypeScript
- Comunicación REST + RabbitMQ async
- RAG con Bedrock Sonnet 4.1

## Ejecutar Sistema

### Prerequisitos
- Docker & Docker Compose
- Python 3.11
- Node.js 18+
- AWS credentials (Bedrock)

### Iniciar Backend
```bash
docker-compose up -d
cd auth-service && uvicorn app.main:app --reload --port 8001
cd user-service && uvicorn app.main:app --reload --port 8002
cd audit-service && python app/consumer.py &
cd ai-service && uvicorn app.main:app --reload --port 8004
```

### Iniciar Frontend
```bash
cd frontend
npm install
npm run dev
```

## Tests
```bash
cd user-service
pytest --cov=app tests/
```

## Endpoints
- Auth: http://localhost:8001
- Users: http://localhost:8002
- AI: http://localhost:8004
- Frontend: http://localhost:5173

## Principios DDD
- Domain entities separadas de infra
- Repositories como abstracciones
- Use cases encapsulan lógica negocio

## Clean Architecture
- 4 capas: Domain, Application, Infrastructure, Presentation
- Dependencias apuntan hacia domain
- Entities agnósticas de frameworks



**sistema completo de gestión de usuarios** con estas funcionalidades principales:

**Sistema base:**
- Login y permisos de usuarios
- Registro de quién accede y cuándo
- Asignación de roles (admin, usuario regular, etc.)

**Interfaz visual:**
- Pantallas para crear, editar y ver usuarios
- Manejo de errores y mensajes al usuario
- Formularios con validaciones

**Inteligencia artificial:**
- Un asistente/agente que responde preguntas sobre los usuarios o genera reportes
- Búsqueda inteligente en documentos usando IA

**Aspectos técnicos clave:**
- Todo debe funcionar en contenedores Docker para ejecutarse fácilmente
- El sistema se divide en partes pequeñas e independientes (microservicios) que se comunican entre sí
- Incluye pruebas automatizadas del código
- Debe registrar lo que sucede para poder diagnosticar problemas

**Resolución de problemas:**
- Analizar y explicar cómo arreglarías errores en el sistema cuando falla

"Implementa el Auth Service completo con login JWT"
"Agrega el endpoint de crear usuario en User Service"
"Crea el componente UserList en React con loading states"
"Implementa RAG en AI Service con Bedrock"

## Resultados de coverage auth-service
- ✅ **13/13 tests pasando**
- 📊 **Coverage: 61%** (de 31% → 61%)

## Áreas con mejor cobertura
- `login_use_case.py`: 100%
- `register_use_case.py`: 100%
- `refresh_token_use_case.py`: 83%
- `auth_dto.py`: 91%

## Para llegar a >70%
Faltan tests de:
- `auth_routes.py`: 50% → agregar tests E2E del flujo completo
- `user_repository_impl.py`: 33% → tests con DB real
- `redis_client.py`: 39% → tests de cache
- `rabbitmq_publisher.py`: 26% → tests de messaging


# Por qué dos bases de datos separadas y diferentes políticas de registro

## Separación de Bases de Datos

**Auth Service DB** y **User Service DB** están separadas por:

1. **Bounded Contexts (DDD)**: 
   - Auth DB: credenciales, tokens, sesiones (contexto de seguridad)
   - User DB: perfiles, roles, metadata (contexto de negocio)

2. **Independencia de Microservicios**:
   - Cada servicio es autónomo y deployable independientemente
   - Fallos aislados (si User Service cae, Auth sigue funcionando)
   - Escalamiento independiente (Auth puede necesitar más réplicas)

3. **Responsabilidades Únicas**:
   - Auth Service: **"¿Quién eres y puedes acceder?"**
   - User Service: **"¿Qué datos tienes y qué puedes hacer?"**

## Diferencia en Políticas de Registro

### `/auth/register` (público)
```python
# Auto-registro de usuarios finales
# NO requiere autenticación
# Rol por defecto: "user"
# Uso: sign-up público en la app
```

**Flujo**:
1. Usuario se registra → crea credenciales en Auth DB
2. Auth publica evento `user.created` → RabbitMQ
3. User Service consume evento → crea perfil en User DB

### `/users` (protegido)
```python
# Creación administrativa de usuarios
# REQUIERE autenticación (JWT)
# Permite asignar roles personalizados (admin, etc.)
# Uso: panel de administración
```

**Flujo**:
1. Admin autenticado llama endpoint
2. User Service valida JWT con Auth Service
3. Crea usuario con rol específico en User DB
4. Publica evento para sincronizar con Auth DB

## Arquitectura Recomendada

```
┌─────────────────┐         ┌──────────────────┐
│  Auth Service   │         │   User Service   │
│  Port 8001      │         │   Port 8002      │
├─────────────────┤         ├──────────────────┤
│ PostgreSQL      │         │ PostgreSQL       │
│ (credentials)   │         │ (profiles)       │
│                 │         │                  │
│ /auth/register  │────────>│ RabbitMQ Event   │
│ (público)       │         │ (sync profile)   │
│                 │         │                  │
│ /auth/login     │<────────│ /users (POST)    │
│ (valida JWT)    │         │ (requiere admin) │
└─────────────────┘         └──────────────────┘
```

## Ventajas del Modelo Actual

- **Seguridad**: Credenciales aisladas de datos de negocio
- **Flexibilidad**: Diferentes estrategias de autenticación sin tocar User Service
- **Auditoría**: Separación clara entre accesos y cambios de perfil
- **Compliance**: Más fácil cumplir GDPR/SOC2 con datos sensibles aislados



# Flujo para crear el primer Admin

## Opción 1: Script de inicialización (RECOMENDADO)

```bash
# Crear script: scripts/create_first_admin.py
```

```python
import asyncio
import sys
sys.path.insert(0, '/app')

from app.infrastructure.database import get_db
from app.domain.entities.user import User
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin():
    db = next(get_db())
    
    # Auth Service - crear credenciales
    hashed = pwd_context.hash("Admin123456")
    auth_user = {
        "id": str(uuid.uuid4()),
        "email": "admin@toka.com",
        "hashed_password": hashed,
        "is_active": True
    }
    # Insertar en auth_db.users
    
    # User Service - crear perfil
    user = User(
        id=auth_user["id"],
        email="admin@toka.com",
        full_name="Super Admin",
        role="admin",
        is_active=True,
        is_verified=True
    )
    # Insertar en users_db.users

create_admin()
```

**Ejecutar:**
```bash
docker exec -it auth-service python scripts/create_first_admin.py
```

## Opción 2: SQL directo

```bash
# En Auth Service DB
docker exec -it postgres psql -U admin -d auth_db

INSERT INTO users (id, email, hashed_password, is_active) 
VALUES (
  'admin-001', 
  'admin@toka.com',
  '$2b$12$...', -- generar con bcrypt
  true
);

# En User Service DB
docker exec -it postgres psql -U admin -d users_db

INSERT INTO users (id, email, full_name, role, is_active, is_verified)
VALUES (
  'admin',
  'admin@toka.com', 
  'Super Admin',
  'admin',
  true,
  true
);
```

## Opción 3: Endpoint especial (bootstrap)

Crear endpoint temporal `/auth/bootstrap` que:
- Solo funciona si no existen usuarios en DB
- Crea admin en Auth Service
- Publica evento para User Service
- Se desactiva automáticamente después

```python
@router.post("/bootstrap")
async def bootstrap_admin(db: Session):
    if db.query(User).count() > 0:
        raise HTTPException(403, "Sistema ya inicializado")
    # Crear admin...
```

**Flujo después del primer admin:**
1. Admin hace login → obtiene JWT
2. Admin crea más usuarios vía `/users` (POST)
3. User Service publica evento
4. Auth Service crea credenciales
5. Nuevos usuarios pueden hacer login