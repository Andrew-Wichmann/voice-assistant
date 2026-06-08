from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, YamlConfigSettingsSource, PydanticBaseSettingsSource


# --- Wake word ---

class OpenWakeWordConfig(BaseModel):
    model: Literal["openWakeWord"]
    wake_word: str
    end_word: str
    threshold: float


WakeWordConfig = Annotated[
    Union[OpenWakeWordConfig],
    Field(discriminator="model"),
]


# --- STT ---

class WhisperSTTConfig(BaseModel):
    model: Literal["whisper"]
    model_id: str


STTConfig = Annotated[
    Union[WhisperSTTConfig],
    Field(discriminator="model"),
]


# --- LLM ---

class OllamaLLMConfig(BaseModel):
    model: Literal["ollama"]
    name: str
    base_url: str = "http://localhost:11434"


class PydanticAILLMConfig(BaseModel):
    model: Literal["pydantic-ai"]
    name: str
    base_url: str = "http://localhost:11434"


LLMConfig = Annotated[
    Union[OllamaLLMConfig, PydanticAILLMConfig],
    Field(discriminator="model"),
]


# --- TTS ---

class PiperTTSConfig(BaseModel):
    model: Literal["piper"]
    voice: str
    model_path: Optional[str] = None


class KokoroTTSConfig(BaseModel):
    model: Literal["kokoro"]
    voice: str


class BarkTTSConfig(BaseModel):
    model: Literal["bark"]
    voice: str


TTSConfig = Annotated[
    Union[PiperTTSConfig, KokoroTTSConfig, BarkTTSConfig],
    Field(discriminator="model"),
]


# --- Root ---

class Config(BaseSettings):
    model_config = {"yaml_file": "config.yaml"}

    wake_word: WakeWordConfig
    stt: STTConfig
    llm: LLMConfig
    tts: TTSConfig

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        **kwargs,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)
