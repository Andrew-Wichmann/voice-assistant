import numpy as np

from app.config import STTConfig
from app.pipeline.stt import STTEngine


class WhisperSTT(STTEngine):
    def __init__(self, config: STTConfig):
        super().__init__(config)
        self._pipeline = None

    def load(self):
        # TODO: initialise transformers Whisper pipeline
        pass

    async def transcribe(self, audio: np.ndarray) -> str:
        # TODO: run inference, return transcript string
        return ""
