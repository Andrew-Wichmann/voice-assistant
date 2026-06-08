# uv add kokoro-onnx
from kokoro_onnx import Kokoro, SAMPLE_RATE

from app.config import KokoroTTSConfig
from app.pipeline.tts import TTSEngine
from app.pipeline.tts.utils import to_pcm16


class KokoroTTS(TTSEngine):
    def __init__(self, config: KokoroTTSConfig):
        super().__init__(config)
        self._kokoro: Kokoro | None = None

    def load(self):
        self._kokoro = Kokoro(
            model_path="voices/kokoro/kokoro-v1.0.onnx",
            voices_path="voices/kokoro/voices-v1.0.bin",
        )

    async def synthesize(self, text: str) -> bytes:
        # config.voice is a Kokoro voice name e.g. "af_heart", "am_adam", "bf_emma"
        audio, sample_rate = self._kokoro.create(text, voice=self.config.voice)
        return to_pcm16(audio, sample_rate)
