from typing import List
import hashlib


class ChunkingService:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, doc_id: str) -> List[dict]:
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunk_id = self._generate_chunk_id(doc_id, i)
            chunks.append({
                "id": chunk_id,
                "content": chunk_text,
                "metadata": {
                    "doc_id": doc_id,
                    "chunk_index": len(chunks),
                    "word_count": len(chunk_words)
                }
            })
        
        return chunks
    
    def _generate_chunk_id(self, doc_id: str, index: int) -> str:
        return hashlib.md5(f"{doc_id}_{index}".encode()).hexdigest()