import pandas as pd
import pandas_ta as ta


class TechnicalIndicators:
    """技术指标计算类"""

    def __init__(self, df: pd.DataFrame):
        """
        初始化技术指标计算器

        Args:
            df: 包含OHLCV数据的DataFrame
        """
        self.df = df.copy()
        self._validate_data()

    def _validate_data(self) -> None:
        """验证输入数据的完整性"""
        required_columns = ["open", "high", "low", "close", "volume"]
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            raise ValueError(f"缺少必要的列: {missing_columns}")

    def calculate_all(self) -> pd.DataFrame:
        """计算所有技术指标"""
        # 移动平均线
        self.df["ma5"] = self.df.ta.sma(length=5)
        self.df["ma10"] = self.df.ta.sma(length=10)
        self.df["ma20"] = self.df.ta.sma(length=20)

        # RSI
        self.df["rsi"] = self.df.ta.rsi(length=14)

        # MACD
        macd = self.df.ta.macd(fast=12, slow=26, signal=9)
        self.df = pd.concat([self.df, macd], axis=1)

        # 布林带
        bollinger = self.df.ta.bbands(length=20)
        self.df = pd.concat([self.df, bollinger], axis=1)

        # 成交量指标
        self.df["obv"] = self.df.ta.obv()

        return self.df

    def get_market_sentiment(self) -> str:
        """
        基于技术指标计算市场情绪

        Returns:
            str: 市场情绪（看涨/看跌/中性）
        """
        if len(self.df) < 20:
            return "中性"

        # 获取最新指标值
        latest = self.df.iloc[-1]
        prev = self.df.iloc[-2]

        # 计算趋势得分
        trend_score = 0

        # MA趋势
        if latest["close"] > latest["ma20"]:
            trend_score += 1
        elif latest["close"] < latest["ma20"]:
            trend_score -= 1

        # RSI趋势
        if latest["rsi"] > 70:
            trend_score -= 1
        elif latest["rsi"] < 30:
            trend_score += 1

        # MACD趋势
        if latest["MACD_12_26_9"] > latest["MACDs_12_26_9"]:
            trend_score += 1
        elif latest["MACD_12_26_9"] < latest["MACDs_12_26_9"]:
            trend_score -= 1

        # 布林带位置
        if latest["close"] > latest["BBU_20_2.0"]:
            trend_score -= 1
        elif latest["close"] < latest["BBL_20_2.0"]:
            trend_score += 1

        # 根据得分判断市场情绪
        if trend_score >= 2:
            return "看涨"
        elif trend_score <= -2:
            return "看跌"
        else:
            return "中性" 