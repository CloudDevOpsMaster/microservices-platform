# AI Service - RAG with Groq & Qdrant

Full-stack RAG implementation using Groq LLMs and Qdrant vector store.

## Quick Start

```bash
# 1. Set up environment
cp .env.example .env
# Edit .env with your GROQ_API_KEY

# 2. Start services
docker-compose up -d

# 3. Health check
curl http://localhost:8004/health
```

## API Endpoints

### Index Document
```bash
curl -X POST http://localhost:8004/documents/index \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your document content here...",
    "title": "Document Title",
    "metadata": {"source": "web"}
  }'
```

### Query RAG
```bash
curl -X POST http://localhost:8004/chat/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is in the documents?",
    "top_k": 5
  }'
```

## Architecture

```
Query → Embed → Qdrant Search → Context → Groq LLM → Response
Document → Chunk (500 tokens) → Embed → Qdrant Index
```

## Testing

```bash
cd ai-service
pytest tests/ -v --cov=app
```

## Configuration

Key settings in `.env`:
- `GROQ_MODEL`: llama-3.3-70b-versatile (default)
- `CHUNK_SIZE`: 500 words
- `TOP_K`: 5 documents retrieved
- `EMBEDDING_MODEL`: all-MiniLM-L6-v2

## Cost Tracking

Groq pricing (per 1M tokens):
- Llama 3.3 70B: $0.59 input, $0.79 output
- ~20x cheaper than Claude Sonnet 4

Metrics returned in every query response.

## Development

```bash
# Local run
cd ai-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8004
```


## Resumen

✅ **Implementación completa:**

1. **Domain Layer** - Entities e interfaces
2. **Infrastructure** - Groq, Qdrant, Embeddings, Metrics
3. **Application** - Use cases RAG Query e Index Document
4. **Presentation** - FastAPI routes
5. **Config** - Settings y Container DI
6. **Tests** - Unit test ejemplo
7. **Docker** - Compose + Dockerfile
8. **Docs** - README y prompts


## Estrategia RAG para Sistema de Gestión de Usuarios

### FASE 1: Preparación de Documentación (Semana 1)

**Indexar en Qdrant:**
```bash
# 1. Documentación técnica
- Arquitectura del sistema (microservicios, APIs)
- Esquemas de base de datos
- Configuraciones Docker/K8s
- Políticas de seguridad y roles

# 2. Documentación operativa
- Procedimientos de troubleshooting
- Logs comunes de errores
- Playbooks de resolución
- FAQs técnicas

# 3. Documentación de negocio
- Casos de uso
- Flujos de usuario
- Reportes tipo
- Métricas KPI
```

**Implementar:**
```python
# Endpoint batch indexing
POST /documents/batch-index
{
  "documents": [
    {
      "content": "La arquitectura usa auth-service (8001)...",
      "title": "Arquitectura Microservicios",
      "metadata": {"type": "technical", "category": "architecture"}
    },
    {
      "content": "Error 401: verificar JWT token en headers...",
      "title": "Troubleshooting Auth",
      "metadata": {"type": "operations", "category": "errors"}
    }
  ]
}
```

### FASE 2: Casos de Uso RAG

**1. Asistente de Troubleshooting**
```python
# Query con filtros específicos
POST /chat/query
{
  "query": "Usuario reporta error 500 al hacer login",
  "top_k": 5,
  "filters": {
    "metadata.category": "errors",
    "metadata.type": "operations"
  }
}

# Respuesta con contexto de logs + soluciones
```

**2. Generador de Reportes**
```python
POST /chat/query
{
  "query": "Genera reporte de usuarios activos últimos 30 días con métricas de sesiones",
  "top_k": 3,
  "filters": {"metadata.category": "reports"}
}

# RAG combina: plantilla de reporte + datos contextuales
```

**3. Búsqueda de Configuración**
```python
POST /chat/query
{
  "query": "¿Cómo configurar rate limiting en el API Gateway?",
  "filters": {"metadata.type": "technical"}
}
```

**4. Asistente de Roles/Permisos**
```python
POST /chat/query
{
  "query": "¿Qué permisos tiene el rol 'editor' y cómo asignarlo?",
  "filters": {"metadata.category": "security"}
}
```

### FASE 3: Integración con Microservicios

**Arquitectura sugerida:**
```
[Frontend] → [API Gateway:8000]
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
[Auth:8001] [Users:8002] [AI:8004]
    ↓           ↓           ↓
  [PostgreSQL] [PostgreSQL] [Qdrant]
```

**Flujo ejemplo - Chat con contexto de usuario:**
```python
# 1. Frontend llama API Gateway
GET /ai/chat?query="mis últimos accesos"
Headers: Authorization: Bearer <jwt>

# 2. Gateway valida token con auth-service
# 3. Extrae user_id del token
# 4. Llama ai-service con contexto:

POST ai-service:8004/chat/query
{
  "query": "últimos accesos del usuario",
  "filters": {"metadata.user_id": "123"},
  "user_context": {
    "user_id": "123",
    "role": "admin"
  }
}

# 5. AI service consulta users-service si necesita datos frescos
GET users-service:8002/users/123/audit-logs

# 6. Combina datos + RAG context → respuesta personalizada
```

### FASE 4: Features Avanzados

**A. Indexación automática de logs**
```python
# Cronjob que lee logs y indexa errores
async def index_error_logs():
    logs = await fetch_logs(last_24h=True)
    error_logs = filter_errors(logs)
    
    for log in error_logs:
        await index_document({
            "content": f"Error: {log.message}\nStack: {log.stack}",
            "title": f"Error {log.error_code}",
            "metadata": {
                "timestamp": log.time,
                "service": log.service,
                "severity": log.level
            }
        })
```

**B. RAG con datos en tiempo real**
```python
class EnhancedRAGUseCase:
    async def execute(self, query: Query, user_context: dict):
        # 1. RAG normal
        rag_response = await self.base_rag.execute(query)
        
        # 2. Si menciona "usuarios activos", llamar users-service
        if "activos" in query.text:
            live_data = await self.users_api.get_active_users()
            rag_response.text += f"\n\nDatos actuales: {live_data}"
        
        return rag_response
```

**C. Observabilidad del AI**
```python
# Tracking de queries
class AIMetrics:
    async def track_query(self, query, response, user_id):
        await metrics_db.insert({
            "query": query,
            "response_time": response.metrics["latency_ms"],
            "cost": response.metrics["cost_usd"],
            "user_id": user_id,
            "sources_used": len(response.sources),
            "timestamp": datetime.now()
        })
        
# Dashboard: queries más comunes, costos, performance
```

### FASE 5: Testing Strategy

**Tests críticos:**
```python
# 1. RAG accuracy
def test_troubleshooting_accuracy():
    query = "Error 401 en login"
    response = rag.query(query)
    assert "JWT" in response.text
    assert "headers" in response.text

# 2. Filtros funcionan
def test_filters_work():
    response = rag.query("errores", filters={"type": "operations"})
    assert all(s.metadata["type"] == "operations" for s in response.sources)

# 3. Integración
@pytest.mark.integration
async def test_full_flow():
    # Index doc → Query → Verify response
```

### FASE 6: Deployment

**docker-compose.yml completo:**
```yaml
services:
  ai-service:
    # ... (ya definido)
    environment:
      - USER_SERVICE_URL=http://user-service:8002
      - AUTH_SERVICE_URL=http://auth-service:8001
  
  user-service:
    build: ./user-service
    ports: ["8002:8002"]
    
  auth-service:
    build: ./auth-service
    ports: ["8001:8001"]
```

### CHECKLIST de Implementación

**Semana 1-2:**
- [ ] Indexar toda documentación técnica
- [ ] Implementar batch indexing endpoint
- [ ] Tests básicos de RAG

**Semana 3:**
- [ ] Integrar AI con auth (validar JWT)
- [ ] Endpoint chat con filtros por rol
- [ ] UI básica de chat

**Semana 4:**
- [ ] Indexación automática de logs
- [ ] Generación de reportes con RAG
- [ ] Métricas y observabilidad

**Mejoras continuas:**
- [ ] Fine-tuning de prompts según feedback
- [ ] Cache de queries comunes (Redis)
- [ ] A/B testing de diferentes top_k