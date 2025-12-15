from app.config import settings
from app.infrastructure.groq.groq_client import GroqClient
from app.infrastructure.qdrant.qdrant_repo import QdrantRepository
from app.infrastructure.embeddings.embedding_service import EmbeddingService
from app.infrastructure.embeddings.chunking import ChunkingService
from app.infrastructure.evaluation.metrics import ResponseEvaluator
from app.application.use_cases.rag_query import RAGQueryUseCase
from app.application.use_cases.index_document import IndexDocumentUseCase


class Container:
    def __init__(self):
        # Infrastructure
        self.groq_client = GroqClient(
            api_key=settings.groq_api_key,
            model_id=settings.groq_model
        )
        
        self.qdrant_repo = QdrantRepository(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            collection_name=settings.qdrant_collection
        )
        
        self.embedding_service = EmbeddingService(
            model_name=settings.embedding_model
        )
        
        self.chunking_service = ChunkingService(
            chunk_size=settings.chunk_size,
            overlap=settings.chunk_overlap
        )
        
        self.evaluator = ResponseEvaluator()
        
        # Use Cases
        self.rag_query_use_case = RAGQueryUseCase(
            llm_provider=self.groq_client,
            vector_store=self.qdrant_repo,
            embedding_service=self.embedding_service,
            evaluator=self.evaluator
        )
        
        self.index_document_use_case = IndexDocumentUseCase(
            vector_store=self.qdrant_repo,
            embedding_service=self.embedding_service,
            chunking_service=self.chunking_service
        )
    
    async def initialize(self):
        await self.qdrant_repo.initialize(vector_size=self.embedding_service.dimension)


container = Container()