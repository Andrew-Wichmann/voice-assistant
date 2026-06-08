import asyncio
import logging
import re
from collections.abc import AsyncGenerator
from enum import Enum, auto

import numpy as np

from app.pipeline import Pipeline
from app.pipeline.wake import WakeWordDetector
from app.pipeline.stt import STTEngine
from app.pipeline.llm import LLMEngine
from app.pipeline.tts import TTSEngine

logger = logging.getLogger(__name__)

Message = dict | bytes


class State(Enum):
    IDLE = auto()       # scanning for wake word
    LISTENING = auto()  # buffering utterance
    PROCESSING = auto() # running STT → LLM → TTS


class AudioSession:
    # Expects 16kHz mono Int16 PCM from the client
    SAMPLE_RATE = 16_000

    def __init__(self, pipeline: Pipeline):
        self.state = State.IDLE
        self._buffer: list[np.ndarray] = []

        self._wake: WakeWordDetector = pipeline.wake_detector
        self._stt: STTEngine = pipeline.stt_engine
        self._llm: LLMEngine = pipeline.llm_engine
        self._tts: TTSEngine = pipeline.tts_engine

    async def process_chunk(self, raw: bytes) -> AsyncGenerator[Message, None]:
        audio = np.frombuffer(raw, dtype=np.int16)

        if self.state == State.IDLE:
            if self._wake.detect_wake(audio):
                self.state = State.LISTENING
                self._buffer = []
                yield {"event": "listening"}

        elif self.state == State.LISTENING:
            self._buffer.append(audio)
            if self._wake.detect_end(audio):
                self.state = State.PROCESSING
                yield {"event": "processing"}
                async for message in self._process_utterance():
                    yield message

    async def _process_utterance(self) -> AsyncGenerator[Message, None]:
        utterance = np.concatenate(self._buffer)
        self._buffer = []

        transcript = await self._stt.transcribe(utterance)
        end_word = self._wake.config.end_word
        transcript = re.sub(rf'\s*{re.escape(end_word)}[.?!]?\s*$', '', transcript, flags=re.IGNORECASE)
        logger.info(f"transcript: {transcript!r}")
        if not transcript:
            logger.warning("No transciption.")
            self.state = State.IDLE
            yield {"event": "idle"}
            return
        response_text = await self._llm.respond(transcript)
        logger.info(f"response: {response_text!r}")
        audio_response = await self._tts.synthesize(response_text)
        yield audio_response

        self.state = State.IDLE
        yield {"event": "idle"}
