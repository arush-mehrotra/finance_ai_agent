"""Stock data fetching service using yfinance."""
import yfinance as yf
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import pandas as pd

class StockDataService:
    """Service for fetching stock market data."""

    @staticmethod
    def get_stock_info(ticker: str) -> Dict[str, Any]:
        """
        Fetch comprehensive stock information.

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')

        Returns:
            Dictionary containing stock information
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            return {
                "ticker": ticker.upper(),
                "name": info.get("longName", "N/A"),
                "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "dividend_yield": info.get("dividendYield"),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
                "volume": info.get("volume"),
                "avg_volume": info.get("averageVolume"),
                "beta": info.get("beta"),
                "earnings_growth": info.get("earningsGrowth"),
                "revenue_growth": info.get("revenueGrowth"),
                "profit_margins": info.get("profitMargins"),
                "operating_margins": info.get("operatingMargins"),
                "return_on_equity": info.get("returnOnEquity"),
                "debt_to_equity": info.get("debtToEquity"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "business_summary": info.get("longBusinessSummary"),
            }
        except Exception as e:
            raise ValueError(f"Error fetching data for {ticker}: {str(e)}")

    @staticmethod
    def get_historical_data(
        ticker: str, period: str = "1y", interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Fetch historical price data.

        Args:
            ticker: Stock ticker symbol
            period: Time period (e.g., '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
            interval: Data interval (e.g., '1m', '5m', '1h', '1d', '1wk', '1mo')

        Returns:
            DataFrame with historical data
        """
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period, interval=interval)
            return hist
        except Exception as e:
            raise ValueError(f"Error fetching historical data for {ticker}: {str(e)}")

    @staticmethod
    def get_price_summary(ticker: str, period: str = "1y") -> Dict[str, Any]:
        """
        Get price summary statistics.

        Args:
            ticker: Stock ticker symbol
            period: Time period for analysis

        Returns:
            Dictionary with price statistics
        """
        try:
            hist = StockDataService.get_historical_data(ticker, period)

            if hist.empty:
                return {"error": "No historical data available"}

            current_price = hist["Close"].iloc[-1]
            period_start_price = hist["Close"].iloc[0]
            period_return = (
                (current_price - period_start_price) / period_start_price
            ) * 100

            return {
                "current_price": round(current_price, 2),
                "period_start_price": round(period_start_price, 2),
                "period_return_pct": round(period_return, 2),
                "period_high": round(hist["High"].max(), 2),
                "period_low": round(hist["Low"].min(), 2),
                "avg_volume": int(hist["Volume"].mean()),
                "volatility": round(hist["Close"].pct_change().std() * 100, 2),
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_financial_metrics(ticker: str) -> Dict[str, Any]:
        """
        Get key financial metrics for analysis.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with financial metrics
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            metrics = {
                "valuation": {
                    "pe_ratio": info.get("trailingPE"),
                    "forward_pe": info.get("forwardPE"),
                    "peg_ratio": info.get("pegRatio"),
                    "price_to_book": info.get("priceToBook"),
                    "price_to_sales": info.get("priceToSalesTrailing12Months"),
                    "enterprise_value": info.get("enterpriseValue"),
                    "ev_to_revenue": info.get("enterpriseToRevenue"),
                    "ev_to_ebitda": info.get("enterpriseToEbitda"),
                },
                "profitability": {
                    "profit_margins": info.get("profitMargins"),
                    "operating_margins": info.get("operatingMargins"),
                    "gross_margins": info.get("grossMargins"),
                    "return_on_equity": info.get("returnOnEquity"),
                    "return_on_assets": info.get("returnOnAssets"),
                },
                "growth": {
                    "earnings_growth": info.get("earningsGrowth"),
                    "revenue_growth": info.get("revenueGrowth"),
                    "earnings_quarterly_growth": info.get("earningsQuarterlyGrowth"),
                },
                "financial_health": {
                    "total_cash": info.get("totalCash"),
                    "total_debt": info.get("totalDebt"),
                    "debt_to_equity": info.get("debtToEquity"),
                    "current_ratio": info.get("currentRatio"),
                    "quick_ratio": info.get("quickRatio"),
                    "free_cash_flow": info.get("freeCashflow"),
                },
            }

            return metrics
        except Exception as e:
            return {"error": str(e)}
