from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class DocumentChunk:
    id: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Document:
    id: str
    content: str
    title: str
    created_at: datetime
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class QueryResponse:
    text: str
    sources: List[DocumentChunk]
    metrics: dict
    model: str