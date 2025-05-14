from typing import Dict, List, Any
import structlog
from datetime import datetime
from app.datasource.adapters.base import BaseAdapter

logger = structlog.get_logger()

class BlockBeatsAdapter(BaseAdapter):
    """BlockBeats适配器"""
    async def fetch_news(self, page: int = 1, size: int = 10) -> List[Dict[str, Any]]:
        """获取新闻数据"""
        try:
            # 添加必要的查询参数
            params = {
                "page": page,
                "size": size,
                "type": "push",  # 获取重要新闻
                "lang": "cn"     # 获取中文新闻
            }
            
            data = await self.fetch(**params)
            if not data:
                logger.error("BlockBeats API返回空数据")
                return []
                
            if data.get("status") != 0:  # 注意：API 使用 status 而不是 code
                error_msg = data.get("message", "未知错误")
                logger.error("BlockBeats API错误", error=error_msg)
                return []
                
            news_list = data.get("data", {}).get("data", [])
            if not news_list:
                logger.warning("BlockBeats API返回空新闻列表")
                return []
                
            # 处理新闻数据
            processed_news = []
            for news in news_list:
                try:
                    # 将 Unix 时间戳转换为 datetime 对象
                    timestamp = int(news.get("create_time", "0"))
                    publish_time = datetime.fromtimestamp(timestamp)
                    
                    processed_news.append({
                        # API 返回字段
                        "title": news.get("title", ""),
                        "content": news.get("content", ""),
                        "link": news.get("link", ""),
                        "publishTime": publish_time,
                        "type": news.get("type", "push"),
                        
                        # 辅助字段
                        "source": "blockbeats",
                        "status": "pending",
                        "processed_at": None
                    })
                except (ValueError, TypeError) as e:
                    logger.error("处理新闻数据失败", error=str(e), news=news)
                    continue
                
            logger.info("成功获取新闻数据", count=len(processed_news))
            return processed_news
            
        except Exception as e:
            logger.error("获取新闻数据失败", error=str(e))
            return [] 