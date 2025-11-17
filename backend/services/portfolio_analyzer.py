"""Portfolio analyzer service that integrates stock data, news, and AI analysis."""
from typing import Dict, Any, Optional
from backend.services.stock_data import StockDataService
from backend.services.news_service import NewsService
from backend.services.ai_agent import AIAgentService


class PortfolioAnalyzer:
    """
    Unified service that combines stock data, news, and AI analysis
    to provide comprehensive investment insights.
    """

    def __init__(
        self,
        anthropic_api_key: str,
        finnhub_api_key: str,
        ai_model: str = "claude-sonnet-4-5-20250929"
    ):
        """
        Initialize portfolio analyzer with all required services.

        Args:
            anthropic_api_key: Anthropic API key for AI analysis
            finnhub_api_key: Finnhub API key for news data
            ai_model: Claude model to use (default: claude-sonnet-4-5-20250929)

        Raises:
            ValueError: If required API keys are missing
        """
        self.stock_service = StockDataService()
        self.news_service = NewsService(api_key=finnhub_api_key)
        self.ai_service = AIAgentService(api_key=anthropic_api_key, model=ai_model)

    def analyze_investment(
        self,
        ticker: str,
        user_question: Optional[str] = None,
        include_recommendation: bool = True
    ) -> Dict[str, Any]:
        """
        Perform comprehensive investment analysis for a stock.

        This is the main entry point that:
        1. Fetches stock data and financial metrics
        2. Retrieves recent news and sentiment
        3. Generates AI-powered analysis
        4. Provides investment recommendation

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            user_question: Optional specific question about the stock
            include_recommendation: Whether to include buy/hold/sell recommendation

        Returns:
            Dictionary with complete analysis including:
                - stock_info: Basic stock information
                - financial_metrics: Detailed financial metrics
                - news_summary: News summary and sentiment
                - ai_analysis: AI-generated analysis
                - recommendation: Investment recommendation (if requested)

        Example:
            >>> analyzer = PortfolioAnalyzer(anthropic_key, finnhub_key)
            >>> result = analyzer.analyze_investment("AAPL")
            >>> print(result['ai_analysis']['analysis'])
            >>> print(result['recommendation']['recommendation'])  # BUY/HOLD/SELL
        """
        try:
            # Step 1: Fetch stock data
            stock_info = self.stock_service.get_stock_info(ticker)
            financial_metrics = self.stock_service.get_financial_metrics(ticker)

            # Step 2: Fetch news and sentiment
            news = self.news_service.get_company_news(ticker, limit=10)
            news_sentiment = self.news_service.get_news_sentiment(ticker)

            # Step 3: Generate AI analysis
            ai_analysis = self.ai_service.analyze_stock(
                ticker=ticker,
                stock_data=stock_info,
                news=news,
                user_question=user_question
            )

            # Step 4: Generate recommendation (if requested)
            recommendation = None
            if include_recommendation:
                recommendation = self.ai_service.generate_recommendation(
                    ticker=ticker,
                    analysis=ai_analysis['analysis'],
                    stock_data=stock_info
                )

            # Combine all results
            return {
                "ticker": ticker,
                "stock_info": {
                    "name": stock_info.get('name'),
                    "current_price": stock_info.get('current_price'),
                    "market_cap": stock_info.get('market_cap'),
                    "pe_ratio": stock_info.get('pe_ratio'),
                    "sector": stock_info.get('sector'),
                    "industry": stock_info.get('industry'),
                },
                "financial_metrics": financial_metrics,
                "news_summary": news_sentiment,
                "ai_analysis": ai_analysis,
                "recommendation": recommendation,
                "success": True
            }

        except Exception as e:
            return {
                "ticker": ticker,
                "error": str(e),
                "success": False
            }

    def answer_question(
        self,
        ticker: str,
        question: str
    ) -> Dict[str, Any]:
        """
        Answer a specific question about a stock.

        Args:
            ticker: Stock ticker symbol
            question: User's question about the stock

        Returns:
            Dictionary with the answer and supporting data

        Example:
            >>> analyzer = PortfolioAnalyzer(anthropic_key, finnhub_key)
            >>> result = analyzer.answer_question("AAPL", "Is this a good long-term investment?")
            >>> print(result['answer'])
        """
        try:
            # Gather context
            stock_info = self.stock_service.get_stock_info(ticker)
            news = self.news_service.get_company_news(ticker, limit=5)

            # Get AI answer
            answer = self.ai_service.answer_question(
                ticker=ticker,
                question=question,
                stock_data=stock_info,
                news=news
            )

            return {
                "ticker": ticker,
                "question": question,
                "answer": answer,
                "stock_price": stock_info.get('current_price'),
                "success": True
            }

        except Exception as e:
            return {
                "ticker": ticker,
                "question": question,
                "error": str(e),
                "success": False
            }

    def compare_stocks(
        self,
        tickers: list[str]
    ) -> Dict[str, Any]:
        """
        Compare multiple stocks side by side.

        Args:
            tickers: List of stock ticker symbols to compare

        Returns:
            Dictionary with comparison data for each stock

        Example:
            >>> analyzer = PortfolioAnalyzer(anthropic_key, finnhub_key)
            >>> result = analyzer.compare_stocks(["AAPL", "GOOGL", "MSFT"])
        """
        comparisons = []

        for ticker in tickers:
            try:
                stock_info = self.stock_service.get_stock_info(ticker)
                news_sentiment = self.news_service.get_news_sentiment(ticker)

                comparisons.append({
                    "ticker": ticker,
                    "name": stock_info.get('name'),
                    "price": stock_info.get('current_price'),
                    "pe_ratio": stock_info.get('pe_ratio'),
                    "market_cap": stock_info.get('market_cap'),
                    "profit_margin": stock_info.get('profit_margins'),
                    "revenue_growth": stock_info.get('revenue_growth'),
                    "news_sentiment": news_sentiment.get('sentiment'),
                    "success": True
                })
            except Exception as e:
                comparisons.append({
                    "ticker": ticker,
                    "error": str(e),
                    "success": False
                })

        return {
            "comparisons": comparisons,
            "count": len(tickers)
        }

    def get_news_summary(
        self,
        ticker: str
    ) -> Dict[str, Any]:
        """
        Get AI-powered news summary for a stock.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with news summary and key insights

        Example:
            >>> analyzer = PortfolioAnalyzer(anthropic_key, finnhub_key)
            >>> result = analyzer.get_news_summary("TSLA")
            >>> print(result['summary'])
        """
        try:
            # Fetch news
            news = self.news_service.get_company_news(ticker, limit=10)

            # Get AI summary
            summary = self.ai_service.summarize_news(ticker, news)

            return {
                "ticker": ticker,
                "summary": summary['summary'],
                "sentiment": summary['sentiment'],
                "key_points": summary['key_points'],
                "article_count": len(news),
                "success": True
            }

        except Exception as e:
            return {
                "ticker": ticker,
                "error": str(e),
                "success": False
            }
