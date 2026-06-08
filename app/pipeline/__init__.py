from app.pipeline import wake, stt, llm, tts
from app.pipeline.wake import WakeWordDetector
from app.pipeline.stt import STTEngine
from app.pipeline.llm import LLMEngine
from app.pipeline.tts import TTSEngine
from app.config import Config

__all__ = ["wake", "stt", "llm", "tts", "Pipeline"]


class Pipeline:
    def __init__(
        self,
        wake_detector: WakeWordDetector,
        stt_engine: STTEngine,
        llm_engine: LLMEngine,
        tts_engine: TTSEngine,
    ):
        self.wake_detector = wake_detector
        self.stt_engine = stt_engine
        self.llm_engine = llm_engine
        self.tts_engine = tts_engine

    @classmethod
    def load(cls, config: Config) -> "Pipeline":
        w = wake.create(config.wake_word)
        w.load()
        s = stt.create(config.stt)
        s.load()
        l = llm.create(config.llm)
        t = tts.create(config.tts)
        t.load()
        return cls(w, s, l, t)
