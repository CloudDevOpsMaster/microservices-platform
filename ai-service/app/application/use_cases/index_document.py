from app.domain.entities.document import Document, DocumentChunk
from app.domain.interfaces.vector_store import VectorStore
from app.infrastructure.embeddings.embedding_service import EmbeddingService
from app.infrastructure.embeddings.chunking import ChunkingService


class IndexDocumentUseCase:
    def __init__(
        self,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        chunking_service: ChunkingService
    ):
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.chunking_service = chunking_service
    
    async def execute(self, document: Document) -> dict:
        # Chunk document
        chunk_dicts = self.chunking_service.chunk_text(document.content, document.id)
        
        # Generate embeddings
        texts = [c["content"] for c in chunk_dicts]
        embeddings = await self.embedding_service.batch_embed(texts)
        
        # Create chunks with embeddings
        chunks = [
            DocumentChunk(
                id=chunk_dict["id"],
                content=chunk_dict["content"],
                embedding=embedding,
                metadata={
                    **chunk_dict["metadata"],
                    "doc_title": document.title,
                    "created_at": document.created_at.isoformat()
                }
            )
            for chunk_dict, embedding in zip(chunk_dicts, embeddings)
        ]
        
        # Store in vector DB
        await self.vector_store.upsert(chunks)
        
        return {
            "doc_id": document.id,
            "chunks_created": len(chunks),
            "total_words": sum(c.metadata["word_count"] for c in chunks)
        }