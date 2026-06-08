import logging
import numpy as np
import openwakeword

from app.config import OpenWakeWordConfig
from app.pipeline.wake import WakeWordDetector

FRAME_SIZE = 1280  # 80ms at 16kHz — minimum chunk size for openwakeword

logger = logging.getLogger(__name__)

class OpenWakeWordDetector(WakeWordDetector):
    def __init__(self, config: OpenWakeWordConfig):
        super().__init__(config)
        self._model: openwakeword.Model | None = None
        self._buffer = np.array([], dtype=np.int16)

    def load(self):
        self._model = openwakeword.Model(vad_threshold=0.5)

    def _predict(self, audio: np.ndarray) -> dict:
        self._buffer = np.concatenate([self._buffer, audio])
        scores = {}
        while len(self._buffer) >= FRAME_SIZE:
            frame, self._buffer = self._buffer[:FRAME_SIZE], self._buffer[FRAME_SIZE:]
            scores.update(self._model.predict(frame))
        return scores

    def detect_wake(self, audio: np.ndarray) -> bool:
        scores = self._predict(audio)
        return scores.get(self.config.wake_word, 0) >= self.config.threshold

    def detect_end(self, audio: np.ndarray) -> bool:
        scores = self._predict(audio)
        return scores.get(self.config.end_word, 0) >= self.config.threshold
