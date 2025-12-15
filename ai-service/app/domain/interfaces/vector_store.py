from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.document import DocumentChunk


class VectorStore(ABC):
    @abstractmethod
    async def upsert(self, chunks: List[DocumentChunk]) -> None:
        pass
    
    @abstractmethod
    async def search(
        self, 
        embedding: List[float], 
        top_k: int = 5,
        filters: dict = None
    ) -> List[DocumentChunk]:
        pass
    
    @abstractmethod
    async def delete(self, chunk_id: str) -> bool:
        pass