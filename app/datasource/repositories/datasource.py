from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.datasource.models.datasource import DataSource
from app.datasource.models.market import News

class DataSourceRepository:
    """数据源仓储层"""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, name: str) -> Optional[DataSource]:
        """根据名称获取数据源"""
        stmt = select(DataSource).where(
            DataSource.name == name,
            DataSource.is_active == True
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_sources(self) -> List[DataSource]:
        """获取所有活跃的数据源"""
        stmt = select(DataSource).where(DataSource.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def save_news(self, news_list: List[Dict[str, Any]], source_name: str) -> None:
        """保存新闻数据"""
        for news_data in news_list:
            # TODO: better check
            # 检查是否已存在
            # 1. 首先通过链接检查（最可靠）
            if news_data.get("link"):
                stmt = select(News).where(News.link == news_data["link"])
                result = await self.session.execute(stmt)
                if result.scalar_one_or_none():
                    continue
            
            # 2. 如果链接不存在，则通过标题、来源和发布时间检查
            stmt = select(News).where(
                and_(
                    News.title == news_data["title"],
                    News.source == source_name,
                    News.create_time == news_data["publishTime"]
                )
            )
            result = await self.session.execute(stmt)
            if result.scalar_one_or_none():
                continue
            
            news = News(
                title=news_data["title"],
                content=news_data.get("content", ""),
                link=news_data.get("link", ""),
                create_time=news_data["publishTime"],
                type=news_data.get("type", "push"),

                source=news_data.get("source"),
                status=news_data.get("status"),
                processed_at=news_data.get("processed_at")
            )
            self.session.add(news)

        await self.session.commit()

    async def update_source_status(self, source_name: str) -> None:
        """更新数据源状态"""
        source = await self.get_by_name(source_name)
        if source:
            source.last_fetch_at = datetime.utcnow()
            await self.session.commit() 