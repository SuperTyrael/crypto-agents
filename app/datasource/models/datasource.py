from datetime import datetime
from typing import Dict, Optional

from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base
from app.core.types import DataSourceType

class DataSource(Base):
    """数据源模型"""
    __tablename__ = "data_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    api_url: Mapped[str] = mapped_column(String(200))
    api_key: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    api_secret: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    config: Mapped[Dict] = mapped_column(JSON, default=dict)
    fetch_interval: Mapped[int] = mapped_column(Integer, default=300)
    last_fetch_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 