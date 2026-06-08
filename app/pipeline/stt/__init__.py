import abc

import numpy as np

from app.config import STTConfig, WhisperSTTConfig


class STTEngine(abc.ABC):
    def __init__(self, config: WhisperSTTConfig):
        self.config = config

    @abc.abstractmethod
    def load(self) -> None: ...

    @abc.abstractmethod
    async def transcribe(self, audio: np.ndarray) -> str: ...


def create(config: STTConfig) -> STTEngine:
    if isinstance(config, WhisperSTTConfig):
        from app.pipeline.stt.whisper import WhisperSTT
        return WhisperSTT(config)
    raise ValueError(f"Unknown STT config: {type(config)!r}")
