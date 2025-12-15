from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.container import container
from app.domain.entities.query import Query

router = APIRouter(prefix="/chat", tags=["chat"])


class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    filters: Optional[dict] = None


class QueryResponseModel(BaseModel):
    text: str
    sources: list
    metrics: dict
    model: str


@router.post("/query", response_model=QueryResponseModel)
async def query_rag(request: QueryRequest):
    try:
        query = Query(
            text=request.query,
            top_k=request.top_k,
            filters=request.filters
        )
        
        response = await container.rag_query_use_case.execute(query)
        
        return QueryResponseModel(
            text=response.text,
            sources=[{"id": s.id, "content": s.content[:200]} for s in response.sources],
            metrics=response.metrics,
            model=response.model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))