from typing import List
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter

from app.domain.interfaces.vector_store import VectorStore
from app.domain.entities.document import DocumentChunk


class QdrantRepository(VectorStore):
    def __init__(self, host: str, port: int, collection_name: str = "documents"):
        self.client = AsyncQdrantClient(host=host, port=port)
        self.collection_name = collection_name
    
    async def initialize(self, vector_size: int):
        collections = await self.client.get_collections()
        if self.collection_name not in [c.name for c in collections.collections]:
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
    
    async def upsert(self, chunks: List[DocumentChunk]) -> None:
        points = [
            PointStruct(
                id=chunk.id,
                vector=chunk.embedding,
                payload={"content": chunk.content, **chunk.metadata}
            )
            for chunk in chunks if chunk.embedding
        ]
        await self.client.upsert(collection_name=self.collection_name, points=points)
    
    async def search(
        self, 
        embedding: List[float], 
        top_k: int = 5,
        filters: dict = None
    ) -> List[DocumentChunk]:
        search_filter = Filter(**filters) if filters else None
        
        results = await self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=top_k,
            query_filter=search_filter
        )
        
        return [
            DocumentChunk(
                id=str(hit.id),
                content=hit.payload["content"],
                metadata={k: v for k, v in hit.payload.items() if k != "content"}
            )
            for hit in results
        ]
    
    async def delete(self, chunk_id: str) -> bool:
        await self.client.delete(
            collection_name=self.collection_name,
            points_selector=[chunk_id]
        )
        return True