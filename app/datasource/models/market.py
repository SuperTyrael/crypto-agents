from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class News(Base):
    """新闻数据模型"""

    __tablename__ = "news_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # API 返回字段
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="新闻标题")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    link: Mapped[str] = mapped_column(String(500), nullable=False, comment="新闻链接")
    create_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="新闻创建时间")
    type: Mapped[str] = mapped_column(String(50), nullable=False, comment="新闻类型")
    
    # 辅助字段
    source: Mapped[str] = mapped_column(String(50), nullable=False, comment="数据来源")
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="新闻摘要")
    sentiment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="情感分析结果")
    status: Mapped[str] = mapped_column(String(20), default="pending", comment="处理状态")
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="处理时间")
    
    # 系统字段
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, comment="记录创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="记录更新时间")

    # 索引
    __table_args__ = (
        Index("idx_news_create_time", "create_time"),
        Index("idx_news_source", "source"),
        Index("idx_news_status", "status"),
    )


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
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 