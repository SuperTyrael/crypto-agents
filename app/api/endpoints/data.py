from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.db import get_session
from app.models.market import News, Kline
from app.models.datasource import DataSource

router = APIRouter()

@router.get("/news")
async def get_news(
    limit: int = 10,
    session: AsyncSession = Depends(get_session)
) -> List[dict]:
    """获取最新新闻"""
    stmt = select(News).order_by(News.published_at.desc()).limit(limit)
    result = await session.execute(stmt)
    news = result.scalars().all()
    return [{"title": n.title, "summary": n.summary, "published_at": n.published_at} for n in news]

@router.get("/klines")
async def get_klines(
    limit: int = 10,
    session: AsyncSession = Depends(get_session)
) -> List[dict]:
    """获取最新K线数据"""
    stmt = select(Kline).order_by(Kline.timestamp.desc()).limit(limit)
    result = await session.execute(stmt)
    klines = result.scalars().all()
    return [{"timestamp": k.timestamp, "open": k.open, "close": k.close} for k in klines]

@router.get("/sources")
async def get_sources(
    session: AsyncSession = Depends(get_session)
) -> List[dict]:
    """获取数据源状态"""
    stmt = select(DataSource)
    result = await session.execute(stmt)
    sources = result.scalars().all()
    return [{
        "name": s.name,
        "type": s.type,
        "last_fetch_time": s.last_fetch_time,
        "is_active": s.is_active
    } for s in sources] 