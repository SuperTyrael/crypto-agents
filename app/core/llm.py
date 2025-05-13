from typing import Dict, List

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

from app.core.config import settings


class LLMAnalyzer:
    """LLM市场分析器"""

    def __init__(self):
        """初始化LLM分析器"""
        self.llm = ChatOpenAI(
            model_name=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
        )

        self.system_prompt = """你是一位专业的加密货币交易顾问。
请基于提供的市场数据和技术指标，给出专业的市场分析和交易建议。
你的分析应该包含：
1. 市场情绪判断（看涨/看跌/中性）及理由
2. 具体的买卖区间建议和置信度（0-100）
3. 潜在风险提示
请用简洁的Markdown格式输出。"""

        self.human_prompt = """最近60分钟BTCUSDT市场数据：
{market_data}

技术指标：
{technical_indicators}

相关新闻：
{news_data}

请给出你的分析。"""

    async def analyze_market(
        self,
        market_data: Dict,
        technical_indicators: Dict,
        news_data: List[Dict],
    ) -> Dict:
        """
        分析市场数据

        Args:
            market_data: 市场数据
            technical_indicators: 技术指标
            news_data: 新闻数据

        Returns:
            Dict: 分析结果
        """
        # 构建提示
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=self.system_prompt),
                HumanMessage(
                    content=self.human_prompt.format(
                        market_data=self._format_market_data(market_data),
                        technical_indicators=self._format_indicators(technical_indicators),
                        news_data=self._format_news(news_data),
                    )
                ),
            ]
        )

        # 调用LLM
        response = await self.llm.agenerate([prompt.format_messages()])
        analysis = response.generations[0][0].text

        # 解析结果
        return {
            "analysis": analysis,
            "sentiment": self._extract_sentiment(analysis),
            "confidence": self._extract_confidence(analysis),
        }

    def _format_market_data(self, data: Dict) -> str:
        """格式化市场数据"""
        return f"""
- 开盘价: {data['open']}
- 最高价: {data['high']}
- 最低价: {data['low']}
- 收盘价: {data['close']}
- 成交量: {data['volume']}
"""

    def _format_indicators(self, indicators: Dict) -> str:
        """格式化技术指标"""
        return f"""
- MA5: {indicators['ma5']}
- MA20: {indicators['ma20']}
- RSI: {indicators['rsi']}
- MACD: {indicators['macd']}
- 布林带: 上轨={indicators['bb_upper']}, 中轨={indicators['bb_middle']}, 下轨={indicators['bb_lower']}
"""

    def _format_news(self, news: List[Dict]) -> str:
        """格式化新闻数据"""
        if not news:
            return "暂无相关新闻"
        return "\n".join([f"- {item['title']}: {item['summary']}" for item in news])

    def _extract_sentiment(self, analysis: str) -> str:
        """从分析中提取市场情绪"""
        if "看涨" in analysis:
            return "看涨"
        elif "看跌" in analysis:
            return "看跌"
        return "中性"

    def _extract_confidence(self, analysis: str) -> int:
        """从分析中提取置信度"""
        # 简单实现，实际应该使用更复杂的解析逻辑
        try:
            confidence_str = analysis.split("置信度")[1].split("%")[0].strip()
            return int(confidence_str)
        except (IndexError, ValueError):
            return 50  # 默认中等置信度 