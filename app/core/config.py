from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类"""

    # 应用配置
    APP_NAME: str = "crypto-agents"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # 数据库配置
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/crypto_agents"

    # API 配置
    BINANCE_API_KEY: str
    BINANCE_API_SECRET: str
    CRYPTOPANIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: str

    # 任务调度配置
    FETCH_MARKET_INTERVAL: int = 60  # 秒
    FETCH_NEWS_INTERVAL: int = 300  # 秒
    CALC_INDICATOR_INTERVAL: int = 300  # 秒
    LLM_ANALYSIS_INTERVAL: int = 3600  # 秒

    # LLM 配置
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings() 