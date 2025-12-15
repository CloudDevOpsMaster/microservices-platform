from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Groq
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"
    
    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "documents"
    
    # Embedding
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 500
    chunk_overlap: int = 50
    
    # RAG
    top_k: int = 5
    max_tokens: int = 1000
    temperature: float = 0.7
    
    # Service
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"


settings = Settings()