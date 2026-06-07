from app.config import TTSConfig
from app.pipeline.tts import TTSEngine


class PiperTTS(TTSEngine):
    def __init__(self, config: TTSConfig):
        super().__init__(config)

    def load(self):
        # TODO: initialise Piper TTS engine
        pass

    async def synthesize(self, text: str) -> bytes:
        # TODO: run TTS inference, return raw PCM bytes
        return open("static/sample.pcm", "rb").read()
