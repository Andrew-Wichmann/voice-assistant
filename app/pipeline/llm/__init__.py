import abc

from app.config import LLMConfig, OllamaLLMConfig


class LLMEngine(abc.ABC):
    def __init__(self, config: OllamaLLMConfig):
        self.config = config

    @abc.abstractmethod
    async def respond(self, text: str) -> str: ...


def create(config: LLMConfig) -> LLMEngine:
    if isinstance(config, OllamaLLMConfig):
        from app.pipeline.llm.ollama import OllamaLLM
        return OllamaLLM(config)
    raise ValueError(f"Unknown LLM config: {type(config)!r}")
