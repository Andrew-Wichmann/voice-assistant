import abc

from app.config import TTSConfig, PiperTTSConfig, KokoroTTSConfig, BarkTTSConfig


class TTSEngine(abc.ABC):
    def __init__(self, config):
        self.config = config

    @abc.abstractmethod
    def load(self) -> None: ...

    @abc.abstractmethod
    async def synthesize(self, text: str) -> bytes: ...


def create(config: TTSConfig) -> TTSEngine:
    if isinstance(config, PiperTTSConfig):
        from app.pipeline.tts.piper import PiperTTS
        return PiperTTS(config)
    if isinstance(config, KokoroTTSConfig):
        from app.pipeline.tts.kokoro import KokoroTTS
        return KokoroTTS(config)
    if isinstance(config, BarkTTSConfig):
        from app.pipeline.tts.bark import BarkTTS
        return BarkTTS(config)
    raise ValueError(f"Unknown TTS config: {type(config)!r}")
