from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from app.container import container
from app.domain.entities.document import Document

router = APIRouter(prefix="/documents", tags=["documents"])


class IndexRequest(BaseModel):
    content: str
    title: str
    metadata: dict = {}


class IndexResponse(BaseModel):
    doc_id: str
    chunks_created: int
    total_words: int


@router.post("/index", response_model=IndexResponse)
async def index_document(request: IndexRequest):
    try:
        doc_id = f"doc_{datetime.utcnow().timestamp()}"
        
        document = Document(
            id=doc_id,
            content=request.content,
            title=request.title,
            created_at=datetime.utcnow(),
            metadata=request.metadata
        )
        
        result = await container.index_document_use_case.execute(document)
        
        return IndexResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))