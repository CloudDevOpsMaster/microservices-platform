import time
from typing import List
from groq import AsyncGroq
from tenacity import retry, stop_after_attempt, wait_exponential

from app.domain.interfaces.llm_provider import LLMProvider
from app.domain.entities.query import LLMResponse, TokenUsage


class GroqClient(LLMProvider):
    def __init__(self, api_key: str, model_id: str = "llama-3.3-70b-versatile"):
        self.client = AsyncGroq(api_key=api_key)
        self.model_id = model_id
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def generate(
        self, 
        messages: List[dict], 
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> LLMResponse:
        start_time = time.time()
        
        try:
            completion = await self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            duration_ms = (time.time() - start_time) * 1000
            
            return LLMResponse(
                text=completion.choices[0].message.content,
                usage=TokenUsage(
                    input_tokens=completion.usage.prompt_tokens,
                    output_tokens=completion.usage.completion_tokens,
                    total_tokens=completion.usage.total_tokens
                ),
                model=completion.model,
                duration_ms=duration_ms
            )
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")