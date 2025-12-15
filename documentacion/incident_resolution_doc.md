# Resolución de Problema: Falla en Sistema de Microservicios

## 📋 DESCRIPCIÓN DEL INCIDENTE

**Reporte inicial:**
- ❌ Usuarios no pueden guardar registros
- ❌ Errores 500 en algunos microservicios
- ❌ Alta latencia en respuestas de agentes IA

**Severidad:** CRÍTICA (P1)
**Impacto:** Funcionalidad principal comprometida

---

## 🔍 FASE 1: HIPÓTESIS INICIALES (Primeros 5 min)

### Hipótesis priorizadas por probabilidad:

**1. Base de datos (ALTA probabilidad)**
- PostgreSQL saturado por conexiones no cerradas
- MongoDB sin índices en colecciones de auditoría
- Redis con memoria llena (eviction de caché)

**2. Comunicación entre servicios (ALTA probabilidad)**
- RabbitMQ con colas saturadas (eventos no procesados)
- Timeouts en llamadas REST entre servicios
- Circuit breakers abiertos por fallos en cascada

**3. Agentes IA (MEDIA-ALTA probabilidad)**
- Rate limiting de APIs (OpenAI/Bedrock)
- Context window excedido (tokens > límite)
- Embeddings pipeline bloqueado
- Vector DB (Qdrant) con consultas lentas

**4. Problemas de red/infraestructura (MEDIA probabilidad)**
- Contenedores Docker sin recursos (CPU/memoria)
- Puertos bloqueados o servicios caídos
- DNS interno de Docker no resuelve nombres

---

## 🛠️ FASE 2: PLAN DE DIAGNÓSTICO SISTEMÁTICO (10 min)

### Paso 1: Verificar estado de servicios (30 seg)
```bash
# Check all containers
docker-compose ps

# Quick health check
curl http://localhost:8001/health  # Auth
curl http://localhost:8002/health  # User
curl http://localhost:8003/health  # Audit
curl http://localhost:8004/health  # AI
```

**Acción:** Identificar qué servicios están caídos o degradados.

---

### Paso 2: Analizar logs estructurados (3 min)

**Prioridad de revisión:**
1. User Service (donde ocurre el error de guardado)
2. AI Service (alta latencia reportada)
3. RabbitMQ (comunicación asíncrona)

```bash
# Logs en tiempo real con filtro de errores
docker-compose logs -f --tail=100 user-service | grep -E "ERROR|500"
docker-compose logs -f --tail=100 ai-service | grep -E "latency|timeout"
docker-compose logs -f rabbitmq | grep -E "queue|overflow"
```

**Buscar en logs JSON:**
- `request_id` para rastrear flujo completo
- `error_type` y `stack_trace`
- `response_time_ms` para identificar cuellos de botella
- `db_query_duration` para problemas de DB

---

### Paso 3: Verificar bases de datos (2 min)

```bash
# PostgreSQL - conexiones activas
docker exec -it postgres psql -U admin -d users_db -c \
  "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"

# PostgreSQL - queries lentas
docker exec -it postgres psql -U admin -d users_db -c \
  "SELECT query, state, wait_event_type FROM pg_stat_activity WHERE state != 'idle';"

# MongoDB - operaciones en curso
docker exec -it mongodb mongosh --eval "db.currentOp()"

# Redis - uso de memoria
docker exec -it redis redis-cli INFO memory | grep used_memory_human
```

**Indicadores críticos:**
- PostgreSQL: >80% conexiones máximas
- MongoDB: operaciones bloqueadas (locks)
- Redis: memoria >90% del límite

---

### Paso 4: Verificar RabbitMQ (1 min)

```bash
# Management UI
# http://localhost:15672 (admin/admin123)

# O via CLI
docker exec -it rabbitmq rabbitmqctl list_queues name messages consumers
```

**Señales de alerta:**
- Colas con >1000 mensajes sin procesar
- Consumidores en 0 (Audit Service caído)
- Rate de mensajes entrantes > rate de procesamiento

---

### Paso 5: Diagnóstico específico de IA (2 min)

```bash
# Logs de AI Service - buscar rate limiting
docker-compose logs ai-service | grep -E "rate_limit|429|quota"

# Verificar latencia de llamadas a Bedrock/OpenAI
docker-compose logs ai-service | grep "llm_call_duration"

# Estado de Qdrant
curl http://localhost:6333/collections
```

**Problemas comunes:**
- HTTP 429: Rate limit excedido
- HTTP 503: Servicio IA temporalmente no disponible
- Latencia >5s: Context window muy grande o embeddings lentos
- Qdrant: Colecciones sin índices optimizados

---

### Paso 6: Verificar recursos de contenedores (1 min)

```bash
# Uso de CPU/memoria por contenedor
docker stats --no-stream

# Eventos de OOM (Out of Memory)
docker inspect user-service | grep -i oom
```

---

## 🎯 FASE 3: DIAGNÓSTICO PROBABLE (Basado en síntomas)

### Escenario A: Error 500 en User Service al guardar

**Diagnóstico más probable:**
1. PostgreSQL con conexiones saturadas
2. SQLAlchemy sin `pool_pre_ping=True` (conexiones muertas)
3. Transacciones no commiteadas bloqueando escrituras

**Solución inmediata:**
```bash
# Reiniciar pool de conexiones
docker-compose restart user-service

# Si persiste, reiniciar PostgreSQL (último recurso)
docker-compose restart postgres
```

**Fix permanente:**
```python
# user-service/app/infrastructure/database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=5,
    pool_pre_ping=True,  # ← Detecta conexiones muertas
    pool_recycle=3600    # ← Recicla cada hora
)
```

---

### Escenario B: Alta latencia en AI Service

**Diagnóstico más probable:**
1. Rate limiting de API (429 errors)
2. Context window excedido (>200K tokens)
3. Qdrant sin índices HNSW optimizados

**Solución inmediata:**
```python
# ai-service/app/infrastructure/groq/groq_client.py
# Agregar retry con exponential backoff
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(RateLimitError)
)
async def generate(self, prompt, context):
    # Limitar context window
    context_tokens = self.count_tokens(context)
    if context_tokens > 100000:  # 50% del límite
        context = self.truncate_context(context, max_tokens=100000)
    
    response = await self.client.generate(...)
```

**Fix Qdrant:**
```python
# Optimizar búsqueda vectorial
client.update_collection(
    collection_name="documents",
    hnsw_config=models.HnswConfigDiff(
        m=16,  # Reduce latencia
        ef_construct=100
    )
)
```

---

### Escenario C: RabbitMQ saturado

**Diagnóstico:**
- Audit Service caído (consumer no procesa)
- Colas con backlog masivo

**Solución:**
```bash
# Reiniciar consumer
docker-compose restart audit-service

# Monitorear procesamiento
watch -n 1 'docker exec rabbitmq rabbitmqctl list_queues'
```

---

## 📊 FASE 4: MÉTRICAS Y MONITOREO

### Logs centralizados a revisar:

```json
// Ejemplo de log estructurado para seguir el flujo
{
  "timestamp": "2025-12-15T10:30:00Z",
  "level": "ERROR",
  "service": "user-service",
  "request_id": "abc-123",
  "user_id": "user-456",
  "endpoint": "/users",
  "method": "POST",
  "status_code": 500,
  "error_type": "DatabaseConnectionError",
  "error_message": "FATAL: remaining connection slots reserved",
  "db_query_duration_ms": 5000,
  "response_time_ms": 5100
}
```

**Usar request_id para rastreo:**
```bash
# Seguir flujo completo de una request fallida
docker-compose logs | grep "abc-123"
```

---

## 📢 FASE 5: COMUNICACIÓN A STAKEHOLDERS

### T+5 min (Update inicial)
**Slack/Email:**
```
🔴 INCIDENTE CRÍTICO - Sistema de usuarios
Estado: Investigando
Impacto: Usuarios no pueden guardar registros
Equipo: Revisando logs de DB y servicios
ETA próximo update: 10 minutos
```

### T+15 min (Diagnóstico)
```
🟡 INCIDENTE EN PROGRESO
Causa identificada: Pool de conexiones PostgreSQL saturado
Acción: Aplicando fix de configuración + reinicio controlado
Impacto: Sistema temporalmente en modo solo-lectura
ETA resolución: 15 minutos
```

### T+30 min (Resolución)
```
🟢 INCIDENTE RESUELTO
Causa raíz: Pool de conexiones sin reciclaje automático
Solución aplicada: Configuración pool_pre_ping + pool_recycle
Estado: Sistema operando normalmente
Monitoreo: Continuamos observando métricas por 2 horas
Post-mortem: Programado para mañana 10am
```

---

## 🔧 ACCIONES PREVENTIVAS

### Corto plazo (esta semana):
1. **Agregar health checks robustos:**
```python
@router.get("/health")
async def health_check(db: Session):
    checks = {
        "database": check_db_connection(db),
        "redis": check_redis_connection(),
        "rabbitmq": check_rabbitmq_connection()
    }
    if not all(checks.values()):
        raise HTTPException(503, detail=checks)
    return {"status": "healthy", "checks": checks}
```

2. **Implementar circuit breakers:**
```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
async def call_ai_service(query):
    # Si falla 5 veces, abre circuito por 60s
    return await ai_client.query(query)
```

3. **Agregar alertas proactivas:**
- CPU >80% por 5 min
- Memoria >85%
- Colas RabbitMQ >500 mensajes
- Latencia P95 >2s

### Mediano plazo (próximo sprint):
1. Implementar APM (Application Performance Monitoring)
2. Logs centralizados en ELK/Loki
3. Dashboards de métricas en Grafana
4. Tests de carga automatizados

---

## ✅ CHECKLIST DE RESOLUCIÓN

- [ ] Identificar servicio(s) afectado(s)
- [ ] Revisar logs estructurados con request_id
- [ ] Verificar estado de DBs (conexiones, queries)
- [ ] Verificar RabbitMQ (colas, consumidores)
- [ ] Diagnosticar problemas de IA (rate limits, latencia)
- [ ] Aplicar fix temporal (restart si es necesario)
- [ ] Validar resolución con tests manuales
- [ ] Comunicar resolución a stakeholders
- [ ] Aplicar fix permanente en código
- [ ] Deploy de fix con tests
- [ ] Monitoreo post-incidente (2 horas)
- [ ] Documentar en post-mortem

---

## 📈 MÉTRICAS POST-INCIDENTE

**Monitorear por 2 horas:**
- Tasa de errores 500: <0.1%
- Latencia P95: <500ms
- Latencia AI Service: <3s
- Uso de conexiones DB: <60%
- Backlog RabbitMQ: <50 mensajes

**SLA objetivo:**
- Tiempo de detección: <5 min
- Tiempo de diagnóstico: <15 min
- Tiempo de resolución: <30 min
- MTTR (Mean Time To Recovery): <1 hora