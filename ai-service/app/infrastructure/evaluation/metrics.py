from app.domain.entities.query import LLMResponse

# Groq pricing per 1M tokens
GROQ_PRICING = {
    "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
    "llama-3.1-70b-versatile": {"input": 0.59, "output": 0.79},
    "mixtral-8x7b-32768": {"input": 0.24, "output": 0.24}
}


class ResponseEvaluator:
    def evaluate(self, response: LLMResponse) -> dict:
        cost = self._calculate_cost(response)
        
        return {
            "latency_ms": response.duration_ms,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.total_tokens,
            "cost_usd": cost,
            "model": response.model
        }
    
    def _calculate_cost(self, response: LLMResponse) -> float:
        pricing = GROQ_PRICING.get(response.model, {"input": 0, "output": 0})
        
        input_cost = (response.usage.input_tokens / 1_000_000) * pricing["input"]
        output_cost = (response.usage.output_tokens / 1_000_000) * pricing["output"]
        
        return round(input_cost + output_cost, 6)