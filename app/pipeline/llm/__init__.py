import abc

from app.config import LLMConfig


class LLMEngine(abc.ABC):
    def __init__(self, config: LLMConfig):
        self.config = config

    @abc.abstractmethod
    async def respond(self, text: str) -> str: ...


def create(config: LLMConfig) -> LLMEngine:
    if config.model == "ollama":
        from app.pipeline.llm.ollama import OllamaLLM
        return OllamaLLM(config)
    raise ValueError(f"Unknown LLM model: {config.model!r}")
