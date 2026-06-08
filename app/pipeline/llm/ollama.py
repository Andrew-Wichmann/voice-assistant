import httpx

from app.config import OllamaLLMConfig
from app.pipeline.llm import LLMEngine

class OllamaLLM(LLMEngine):
    def __init__(self, config: OllamaLLMConfig):
        super().__init__(config)

    async def respond(self, text: str) -> str:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(f"{self.config.base_url}/api/chat", json={
                "model": self.config.name,
                "messages": [{"role": "user", "content": text}],
                "stream": False,
            })
            response.raise_for_status()
            return response.json()["message"]["content"]
