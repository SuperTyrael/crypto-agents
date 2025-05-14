from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类"""

    # 应用配置
    APP_NAME: str = "crypto-agents"
    ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # 数据库配置
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/crypto_agents"
    DB_ECHO: bool = False  # 是否打印SQL语句

    # API 配置
    BINANCE_API_KEY: str = "your-api-key"
    BINANCE_API_SECRET: str = "your-api-secret"
    CRYPTOPANIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: str = "your-api-key"
    OPENAI_MODEL: str = "gpt-4"

    # 任务调度配置
    FETCH_MARKET_INTERVAL: int = 60  # 秒
    FETCH_NEWS_INTERVAL: int = 300  # 秒
    CALC_INDICATOR_INTERVAL: int = 300  # 秒
    LLM_ANALYSIS_INTERVAL: int = 3600  # 秒

    # LLM 配置
    LLM_MODEL: str = "gpt-3.5-turbo"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1000

    # 数据源配置
    BLOCKBEATS_API_URL: str = "https://api.theblockbeats.news/v1/open-api/open-flash"
    BLOCKBEATS_FETCH_INTERVAL: int = 300  # 5分钟
    MARKET_FETCH_INTERVAL: int = 60       # 1分钟
    INDICATOR_CALC_INTERVAL: int = 300    # 5分钟

    # 监控配置
    ENABLE_METRICS: bool = True
    PROMETHEUS_PORT: int = 9090

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings() 