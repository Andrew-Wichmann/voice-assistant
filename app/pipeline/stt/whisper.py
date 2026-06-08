import numpy as np
from transformers import pipeline, WhisperTokenizer

from app.config import WhisperSTTConfig
from app.pipeline.stt import STTEngine

SAMPLE_RATE = 16_000


class WhisperSTT(STTEngine):
    def __init__(self, config: WhisperSTTConfig):
        super().__init__(config)
        self._pipeline = None

    def load(self):
        # config.size e.g. "base.en", "small.en", "medium.en", "large-v3"
        model_id = self.config.model_id
        tokenizer = WhisperTokenizer.from_pretrained(
            model_id, clean_up_tokenization_spaces=False
        )
        self._pipeline = pipeline(
            "automatic-speech-recognition",
            model=model_id,
            tokenizer=tokenizer,
        )

    async def transcribe(self, audio: np.ndarray) -> str:
        float_audio = audio.astype(np.float32) / 32768.0
        result = self._pipeline({"array": float_audio, "sampling_rate": SAMPLE_RATE})
        return result["text"].strip()
