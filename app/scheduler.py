import asyncio
import logging
from datetime import datetime

import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import async_session_factory
from app.datasource.services.datasource import DataSourceService
from app.core.types import DataSourceType

# 配置日志
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = structlog.get_logger()


class JobScheduler:
    """任务调度器"""

    def __init__(self):
        """初始化调度器"""
        self.scheduler = AsyncIOScheduler()
        self.data_source_service = None
        self._setup_jobs()

    async def _init_data_sources(self):
        """初始化数据源服务"""
        try:
            async with async_session_factory() as session:
                self.data_source_service = DataSourceService(session)
                # 注册默认数据源
                await self.data_source_service.register_default_sources()
                logger.info("数据源服务初始化成功")
        except Exception as e:
            logger.error("数据源服务初始化失败", error=str(e))
            raise

    def _setup_jobs(self):
        """设置定时任务"""
        # 新闻数据获取任务
        self.scheduler.add_job(
            self._fetch_news_job,
            CronTrigger(minute=f"*/{settings.BLOCKBEATS_FETCH_INTERVAL // 60}"),
            id="fetch_news",
            name="获取新闻数据",
        )

    async def _fetch_news_job(self):
        """新闻数据获取任务"""
        try:
            async with async_session_factory() as session:
                service = DataSourceService(session)
                # 获取所有活跃的数据源
                sources = await service.repository.get_active_sources()
                for source in sources:
                    try:
                        await service.fetch_and_save_news(source.name)
                        logger.info("新闻数据获取任务完成", source=source.name)
                    except Exception as e:
                        logger.error("新闻数据获取任务失败", source=source.name, error=str(e))
        except Exception as e:
            logger.error("新闻数据获取任务失败", error=str(e))

    async def start(self):
        """启动调度器"""
        try:
            await self._init_data_sources()
            self.scheduler.start()
            logger.info("任务调度器已启动")
        except Exception as e:
            logger.error("调度器启动失败", error=str(e))
            raise

    async def shutdown(self):
        """关闭调度器"""
        try:
            self.scheduler.shutdown()
            logger.info("任务调度器已关闭")
        except Exception as e:
            logger.error("调度器关闭失败", error=str(e))
            raise


async def main():
    """主函数"""
    scheduler = JobScheduler()
    await scheduler.start()

    try:
        # 保持程序运行
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main()) 