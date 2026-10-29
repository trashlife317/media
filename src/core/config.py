import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Config(BaseSettings):
    # Kalshi Configuration (Strictly Required for Live)
    KALSHI_EMAIL: str = Field(...)
    KALSHI_PASSWORD: str = Field(...)
    KALSHI_ENV: str = Field(default="demo")

    # Generic Crypto Configuration (Strictly Required)
    EXCHANGE_API_KEY: str = Field(...)
    EXCHANGE_SECRET: str = Field(...)
    EXCHANGE_NAME: str = Field(default="binance")

    # AI Configuration (Strictly Required)
    OPENAI_API_KEY: str = Field(...)

    # Risk Management limits
    MAX_POSITION_SIZE: float = Field(default=0.05, ge=0.0, le=1.0)
    MAX_DRAWDOWN: float = Field(default=0.10, ge=0.0, le=1.0)
    BASE_CURRENCY: str = Field(default="USDT") # Changed from USD to USDT to align with Crypto pairs

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

config = Config()
