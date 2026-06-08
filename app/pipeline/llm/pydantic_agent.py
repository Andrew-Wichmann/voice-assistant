from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from app.config import PydanticAILLMConfig
from app.pipeline.llm import LLMEngine
from app.tools import load_tools


class PydanticAILLM(LLMEngine):
    def __init__(self, config: PydanticAILLMConfig):
        super().__init__(config)
        provider = OllamaProvider(base_url=f"{config.base_url}/v1")
        model = OllamaModel(config.name, provider=provider)
        self._agent = Agent(model, tools=load_tools())
        self._history: list[ModelMessage] = []

    async def respond(self, text: str) -> str:
        result = await self._agent.run(text, message_history=self._history)
        self._history = list(result.all_messages())
        return str(result.output)
