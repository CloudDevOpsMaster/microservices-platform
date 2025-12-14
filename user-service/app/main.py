from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.presentation.routes import user_routes
from app.infrastructure.database.database import Database
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    db = Database(settings.DATABASE_URL)
    await db.create_tables()
    print("✅ Database tables created")
    
    yield
    
    # Shutdown
    print("👋 Shutting down User Service")


app = FastAPI(
    title="User Service API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(user_routes.router)


@app.get("/")
async def root():
    return {"message": "User Service API", "version": "1.0.0"}