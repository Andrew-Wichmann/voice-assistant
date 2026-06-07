from pydantic import BaseModel
from pydantic_settings import BaseSettings, YamlConfigSettingsSource, PydanticBaseSettingsSource


class WakeWordConfig(BaseModel):
    model: str
    wake_word: str
    end_word: str
    threshold: float


class STTConfig(BaseModel):
    model: str
    size: str


class LLMConfig(BaseModel):
    model: str
    name: str


class TTSConfig(BaseModel):
    model: str
    voice: str


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
