from app.config import LLMConfig
from app.pipeline.llm import LLMEngine


class OllamaLLM(LLMEngine):
    def __init__(self, config: LLMConfig):
        super().__init__(config)

    async def respond(self, text: str) -> str:
        # TODO: call Ollama HTTP API, return response text
        return ""
