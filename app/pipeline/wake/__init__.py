import abc

import numpy as np

from app.config import WakeWordConfig, OpenWakeWordConfig


class WakeWordDetector(abc.ABC):
    def __init__(self, config: OpenWakeWordConfig):
        self.config = config

    @abc.abstractmethod
    def load(self) -> None: ...

    @abc.abstractmethod
    def detect_wake(self, audio: np.ndarray) -> bool: ...

    @abc.abstractmethod
    def detect_end(self, audio: np.ndarray) -> bool: ...


def create(config: WakeWordConfig) -> WakeWordDetector:
    if isinstance(config, OpenWakeWordConfig):
        from app.pipeline.wake.openwakeword import OpenWakeWordDetector
        return OpenWakeWordDetector(config)
    raise ValueError(f"Unknown wake word config: {type(config)!r}")
