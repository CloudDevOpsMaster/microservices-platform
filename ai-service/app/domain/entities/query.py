from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Query:
    text: str
    top_k: int = 5
    filters: Optional[dict] = None
    

@dataclass
class LLMResponse:
    text: str
    usage: 'TokenUsage'
    model: str
    duration_ms: float


@dataclass
class TokenUsage:
    input_tokens: int
    output_tokens: int
    total_tokens: int