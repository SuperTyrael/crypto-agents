from typing import Dict, Any
import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.datasource.services.datasource import DataSourceService
from app.core.db import async_session

logger = structlog.get_logger()

class DataSourceJob:
    """数据源任务"""
    def __init__(self):
        self.scheduler = AsyncIOScheduler(
            jobstores={
                'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
            }
        )
        self._service = None

    @property
    async def service(self) -> DataSourceService:
        """获取数据源服务"""
        if not self._service:
            async with async_session() as session:
                self._service = DataSourceService(session)
        return self._service

    async def fetch_news_job(self, source_name: str) -> None:
        """获取新闻任务"""
        try:
            service = await self.service
            await service.fetch_and_save_news(source_name)
        except Exception as e:
            logger.error(
                "获取新闻任务失败",
                source=source_name,
                error=str(e)
            )

    def add_news_job(self, source_name: str, interval: int) -> None:
        """添加新闻获取任务"""
        self.scheduler.add_job(
            self.fetch_news_job,
            trigger=IntervalTrigger(seconds=interval),
            args=[source_name],
            id=f"fetch_news_{source_name}",
            replace_existing=True
        )

    def start(self) -> None:
        """启动调度器"""
        self.scheduler.start()
        logger.info("数据源任务调度器已启动")

    def shutdown(self) -> None:
        """关闭调度器"""
        self.scheduler.shutdown()
        logger.info("数据源任务调度器已关闭") 