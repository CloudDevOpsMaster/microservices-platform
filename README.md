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

**Auth Service está funcional y bien testeado.** ¿Implementamos el User Service ahora?