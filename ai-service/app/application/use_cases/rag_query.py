# app/domain/entities/query.py
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from app.domain.entities.document import DocumentChunk


@dataclass
class Query:
    text: str
    top_k: int = 5
    filters: Optional[Dict[str, Any]] = None


@dataclass
class QueryResponse:
    text: str
    sources: List[DocumentChunk]
    metrics: Dict[str, Any]
    model: str