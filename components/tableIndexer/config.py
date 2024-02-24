from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    table_detection_score_threshold: float = Field(
        env="TABLE_DETECTION_SCORE_THRESHOLD"
    )
    table_detection_model_repository: str = Field(
        env="TABLE_DETECTION_MODEL_REPOSITORY"
    )
    device_type: str = Field(env="DEVICE_TYPE")
    table_crop_padding: int = Field(env="TABLE_CROP_PADDING")
    table_transformer_model_repository: str = Field(
        env="TABLE_TRANSFORMER_MODEL_REPOSITORY"
    )
    table_reader_languages: List[str] = Field(env="TABLE_READER_LANGUAGES")


SETTINGS = Settings()
