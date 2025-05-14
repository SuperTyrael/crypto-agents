from typing import Dict, List, Optional, Type, Any
import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.datasource.models.datasource import DataSource
from app.datasource.repositories.datasource import DataSourceRepository
from app.datasource.adapters.base import BaseAdapter
from app.datasource.adapters.blockbeats import BlockBeatsAdapter
from app.core.types import DataSourceType, DataSourceProtocol

logger = structlog.get_logger()

class DataSourceService:
    """数据源服务层"""
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = DataSourceRepository(session)
        self._adapters: Dict[str, DataSourceProtocol] = {}
        # TODO: 从配置文件中读取默认数据源
        self._default_sources = {
            "blockbeats": {
                "name": "blockbeats",
                "type": DataSourceType.BLOCKBEATS.value,
                "api_url": "https://api.theblockbeats.news/v1/open-api/open-flash",
                "fetch_interval": 300,
                "is_active": True
            }
        }

    async def register_default_sources(self) -> None:
        """注册默认数据源"""
        for source_config in self._default_sources.values():
            await self.register_source(**source_config)

    async def register_source(
        self,
        name: str,
        type: str,
        api_url: str,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        config: Dict[str, Any] = None,
        fetch_interval: int = 300,
        is_active: bool = True
    ) -> DataSource:
        """注册数据源"""
        # 检查是否已存在
        existing = await self.repository.get_by_name(name)
        if existing:
            logger.info("数据源已存在，更新配置", source=name)
            existing.type = type
            existing.api_url = api_url
            existing.api_key = api_key
            existing.api_secret = api_secret
            existing.config = config or {}
            existing.fetch_interval = fetch_interval
            existing.is_active = is_active
            await self.session.commit()
            return existing

        # 创建新数据源
        source = DataSource(
            name=name,
            type=type,
            api_url=api_url,
            api_key=api_key,
            api_secret=api_secret,
            config=config or {},
            fetch_interval=fetch_interval,
            is_active=is_active
        )
        self.session.add(source)
        await self.session.commit()
        logger.info("数据源注册成功", source=name)
        return source

    async def get_adapter(self, source_name: str) -> Optional[DataSourceProtocol]:
        """获取数据源适配器"""
        if source_name not in self._adapters:
            source = await self.repository.get_by_name(source_name)
            if not source:
                return None
            
            adapter_class = self._get_adapter_class(DataSourceType(source.type))
            if not adapter_class:
                return None
                
            self._adapters[source_name] = adapter_class(source)
            
        return self._adapters[source_name]

    def _get_adapter_class(self, source_type: DataSourceType) -> Optional[Type[DataSourceProtocol]]:
        """根据类型获取适配器类"""
        adapters = {
            DataSourceType.BLOCKBEATS: BlockBeatsAdapter,
            # 添加其他数据源适配器
        }
        return adapters.get(source_type)

    async def fetch_news(self, source_name: str, **kwargs) -> List[Dict[str, Any]]:
        """获取新闻数据"""
        adapter = await self.get_adapter(source_name)
        if not adapter:
            raise ValueError(f"数据源不存在或未激活: {source_name}")
            
        try:
            return await adapter.fetch_news(**kwargs)
        finally:
            await adapter.close()

    async def fetch_and_save_news(self, source_name: str, **kwargs) -> None:
        """获取并保存新闻数据"""
        try:
            # 获取数据
            news_list = await self.fetch_news(source_name, **kwargs)
            
            # 保存数据
            await self.repository.save_news(news_list, source_name)
            
            # 更新状态
            await self.repository.update_source_status(source_name)
            
            logger.info(
                "成功获取并保存新闻数据",
                source=source_name,
                count=len(news_list)
            )
        except Exception as e:
            logger.error(
                "获取新闻数据失败",
                source=source_name,
                error=str(e)
            )
            raise 