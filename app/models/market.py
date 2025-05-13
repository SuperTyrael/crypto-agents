from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """SQLAlchemy 基类"""
    pass


class Kline(Base):
    """K线数据模型"""

    __tablename__ = "kline_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    open: Mapped[float] = mapped_column(Float)
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)
    volume: Mapped[float] = mapped_column(Float)

    # 技术指标
    ma5: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ma10: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    ma20: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rsi: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    macd: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    macd_signal: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    macd_hist: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bb_upper: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bb_middle: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bb_lower: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    obv: Mapped[Optional[float]] = mapped_column(Float, nullable=True)


class News(Base):
    """新闻数据模型"""

    __tablename__ = "news_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(String(500))
    source: Mapped[str] = mapped_column(String(50))
    published_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    sentiment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)


class MarketAnalysis(Base):
    """市场分析结果模型"""

    __tablename__ = "market_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    symbol: Mapped[str] = mapped_column(String(20), index=True)
    analysis: Mapped[str] = mapped_column(Text)
    sentiment: Mapped[str] = mapped_column(String(20))
    confidence: Mapped[int] = mapped_column(Integer)
    technical_sentiment: Mapped[str] = mapped_column(String(20))
    news_sentiment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True) 