# uv add suno-bark
import numpy as np
from bark import SAMPLE_RATE, generate_audio, preload_models

from app.config import BarkTTSConfig
from app.pipeline.tts import TTSEngine
from app.pipeline.tts.utils import to_pcm16


class BarkTTS(TTSEngine):
    def __init__(self, config: BarkTTSConfig):
        super().__init__(config)

    def load(self):
        preload_models()

    async def synthesize(self, text: str) -> bytes:
        # config.voice is a Bark voice preset e.g. "v2/en_speaker_6"
        audio = generate_audio(text, history_prompt=self.config.voice)
        return to_pcm16(audio.astype(np.float32), SAMPLE_RATE)
