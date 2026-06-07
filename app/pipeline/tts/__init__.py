import abc

from app.config import TTSConfig


class TTSEngine(abc.ABC):
    def __init__(self, config: TTSConfig):
        self.config = config

    @abc.abstractmethod
    def load(self) -> None: ...

    @abc.abstractmethod
    async def synthesize(self, text: str) -> bytes: ...


def create(config: TTSConfig) -> TTSEngine:
    if config.model == "piper":
        from app.pipeline.tts.piper import PiperTTS
        return PiperTTS(config)
    raise ValueError(f"Unknown TTS model: {config.model!r}")
