from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.query import LLMResponse


class LLMProvider(ABC):
    @abstractmethod
    async def generate(
        self, 
        messages: List[dict], 
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> LLMResponse:
        pass