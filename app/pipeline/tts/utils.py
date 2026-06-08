from math import gcd

import numpy as np
from scipy.signal import resample_poly

TARGET_RATE = 16_000


def to_pcm16(audio: np.ndarray, src_rate: int) -> bytes:
    if audio.dtype != np.float32:
        audio = audio.astype(np.float32)

    if src_rate != TARGET_RATE:
        g = gcd(src_rate, TARGET_RATE)
        audio = resample_poly(audio, TARGET_RATE // g, src_rate // g)

    return (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16).tobytes()
