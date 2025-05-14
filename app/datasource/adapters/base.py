from typing import Dict, Any
import aiohttp
import structlog
from app.datasource.models.datasource import DataSource
from app.core.types import DataSourceProtocol

logger = structlog.get_logger()

class BaseAdapter(DataSourceProtocol):
    """数据源适配器基类"""
    def __init__(self, source: DataSource):
        self.source = source
        self.session = aiohttp.ClientSession()

    async def fetch(self, **kwargs) -> Dict[str, Any]:
        """获取原始数据"""
        try:
            headers = self._get_headers()
            logger.info("发送API请求", url=self.source.api_url, params=kwargs)
            
            async with self.session.get(
                self.source.api_url,
                headers=headers,
                params=kwargs,
                timeout=30  # 设置超时时间
            ) as response:
                if response.status != 200:
                    error_msg = f"API请求失败: HTTP {response.status}"
                    logger.error(error_msg, url=self.source.api_url)
                    return {}
                    
                try:
                    data = await response.json()
                    logger.debug("API响应数据", data=data)
                    return data
                except Exception as e:
                    logger.error("解析API响应失败", error=str(e))
                    return {}
                    
        except aiohttp.ClientError as e:
            logger.error("API请求异常", error=str(e))
            return {}
        except Exception as e:
            logger.error("未知错误", error=str(e))
            return {}

    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = {
            "User-Agent": "CryptoAgents/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if self.source.api_key:
            headers["X-API-KEY"] = self.source.api_key
        return headers

    async def close(self) -> None:
        """关闭会话"""
        try:
            await self.session.close()
        except Exception as e:
            logger.error("关闭会话失败", error=str(e)) 