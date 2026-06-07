import abc

import numpy as np

from app.config import STTConfig


class STTEngine(abc.ABC):
    def __init__(self, config: STTConfig):
        self.config = config

    @abc.abstractmethod
    def load(self) -> None: ...

    @abc.abstractmethod
    async def transcribe(self, audio: np.ndarray) -> str: ...


def create(config: STTConfig) -> STTEngine:
    if config.model == "whisper":
        from app.pipeline.stt.whisper import WhisperSTT
        return WhisperSTT(config)
    raise ValueError(f"Unknown STT model: {config.model!r}")
