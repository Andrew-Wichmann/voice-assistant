# uv add piper-tts
import numpy as np
from piper.voice import PiperVoice

from app.config import PiperTTSConfig
from app.pipeline.tts import TTSEngine
from app.pipeline.tts.utils import to_pcm16


class PiperTTS(TTSEngine):
    def __init__(self, config: PiperTTSConfig):
        super().__init__(config)
        self._voice: PiperVoice | None = None
        self._sample_rate: int = 16_000

    def load(self):
        self._voice = PiperVoice.load(self.config.model_path)
        self._sample_rate = self._voice.config.sample_rate

    async def synthesize(self, text: str) -> bytes:
        raw = b"".join(chunk.audio_int16_bytes for chunk in self._voice.synthesize(text))
        if self._sample_rate == 16_000:
            return raw
        audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32767
        return to_pcm16(audio, self._sample_rate)
