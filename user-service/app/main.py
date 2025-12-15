"""Main application for User Service."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.routes import user_routes
from app.core.config import settings

app = FastAPI(
    title="User Service",
    description="User management microservice",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routes.router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "user-service",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)