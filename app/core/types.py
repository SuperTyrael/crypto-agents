from enum import Enum
from typing import Dict, Any, Protocol, List

class DataSourceType(str, Enum):
    """数据源类型"""
    BLOCKBEATS = "blockbeats"
    BINANCE = "binance"
    COINGLASS = "coinglass"

class DataSourceConfig(Dict[str, Any]):
    """数据源配置基类"""
    pass

class DataSourceProtocol(Protocol):
    """数据源协议"""
    async def fetch(self, **kwargs) -> Dict[str, Any]:
        """获取数据"""
        ...

    async def close(self) -> None:
        """关闭连接"""
        ...

    async def fetch_news(self, **kwargs) -> List[Dict[str, Any]]:
        """获取新闻数据"""
        ... 