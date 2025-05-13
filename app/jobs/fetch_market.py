import asyncio
from datetime import datetime, timezone
from typing import List

import structlog
from binance import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.market import Kline

logger = structlog.get_logger()


async def fetch_market_data(session: AsyncSession) -> None:
    """
    从Binance获取市场数据并保存到数据库

    Args:
        session: 数据库会话
    """
    try:
        # 初始化Binance客户端
        client = await AsyncClient.create(
            settings.BINANCE_API_KEY,
            settings.BINANCE_API_SECRET,
        )

        # 获取BTCUSDT的1分钟K线数据
        klines = await client.get_klines(
            symbol="BTCUSDT",
            interval="1m",
            limit=1,
        )

        # 转换数据格式
        kline_data = []
        for k in klines:
            kline = Kline(
                symbol="BTCUSDT",
                timestamp=datetime.fromtimestamp(k[0] / 1000, tz=timezone.utc),
                open=float(k[1]),
                high=float(k[2]),
                low=float(k[3]),
                close=float(k[4]),
                volume=float(k[5]),
            )
            kline_data.append(kline)

        # 检查是否已存在相同时间戳的数据
        for kline in kline_data:
            stmt = select(Kline).where(
                Kline.symbol == kline.symbol,
                Kline.timestamp == kline.timestamp,
            )
            result = await session.execute(stmt)
            existing = result.scalar_one_or_none()

            if existing is None:
                session.add(kline)
                logger.info(
                    "新增K线数据",
                    symbol=kline.symbol,
                    timestamp=kline.timestamp,
                )
            else:
                logger.info(
                    "K线数据已存在",
                    symbol=kline.symbol,
                    timestamp=kline.timestamp,
                )

        await session.commit()
        logger.info("市场数据获取完成")

    except Exception as e:
        logger.error("市场数据获取失败", error=str(e))
        raise
    finally:
        await client.close_connection()


async def main():
    """主函数"""
    from app.core.db import async_session_factory

    async with async_session_factory() as session:
        await fetch_market_data(session)


if __name__ == "__main__":
    asyncio.run(main()) 