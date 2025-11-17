"""News fetching service using Finnhub API."""
import finnhub
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


class NewsService:
    """Service for fetching financial news and sentiment data using Finnhub."""

    def __init__(self, api_key: str):
        """
        Initialize news service.

        Args:
            api_key: Finnhub API key (required)

        Raises:
            ValueError: If API key is not provided
        """
        if not api_key:
            raise ValueError("Finnhub API key is required")

        self.api_key = api_key
        self.client = finnhub.Client(api_key=api_key)

    def get_company_news(
        self,
        ticker: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Fetch news articles for a specific company/ticker.

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            from_date: Start date in YYYY-MM-DD format (default: 7 days ago)
            to_date: End date in YYYY-MM-DD format (default: today)
            limit: Maximum number of articles to return

        Returns:
            List of news articles with metadata

        Example:
            >>> service = NewsService("your_api_key")
            >>> news = service.get_company_news("AAPL", from_date="2024-01-01", to_date="2024-01-31")
        """
        # Set default dates if not provided
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")
        if not from_date:
            from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        try:
            articles = self.client.company_news(ticker.upper(), _from=from_date, to=to_date)

            # Format the response
            formatted_articles = []
            for article in articles[:limit]:
                formatted_articles.append({
                    "title": article.get("headline", ""),
                    "description": article.get("summary", ""),
                    "url": article.get("url", ""),
                    "published_at": datetime.fromtimestamp(article.get("datetime", 0)).isoformat(),
                    "source": article.get("source", "Unknown"),
                    "category": article.get("category", "general"),
                    "image": article.get("image", ""),
                    "related_tickers": article.get("related", ticker),
                    "sentiment": self._extract_sentiment(article),
                })

            return formatted_articles

        except Exception as e:
            raise ValueError(f"Error fetching news for {ticker}: {str(e)}")

    def get_market_news(
        self,
        category: str = "general",
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Fetch general market news.

        Args:
            category: News category (general, forex, crypto, merger)
            limit: Maximum number of articles to return

        Returns:
            List of market news articles

        Example:
            >>> service = NewsService("your_api_key")
            >>> news = service.get_market_news(category="general")
        """
        try:
            articles = self.client.general_news(category, min_id=0)

            formatted_articles = []
            for article in articles[:limit]:
                formatted_articles.append({
                    "title": article.get("headline", ""),
                    "description": article.get("summary", ""),
                    "url": article.get("url", ""),
                    "published_at": datetime.fromtimestamp(article.get("datetime", 0)).isoformat(),
                    "source": article.get("source", "Unknown"),
                    "category": article.get("category", category),
                    "image": article.get("image", ""),
                })

            return formatted_articles

        except Exception as e:
            raise ValueError(f"Error fetching market news: {str(e)}")

    def get_news_sentiment(self, ticker: str) -> Dict[str, Any]:
        """
        Get news sentiment analysis for a ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with sentiment analysis and recent news

        Example:
            >>> service = NewsService("your_api_key")
            >>> sentiment = service.get_news_sentiment("AAPL")
        """
        # Get recent news (last 7 days)
        news = self.get_company_news(ticker, limit=10)

        if not news:
            return {
                "ticker": ticker,
                "sentiment": "neutral",
                "sentiment_score": 0.0,
                "article_count": 0,
                "recent_news": [],
                "positive_mentions": 0,
                "negative_mentions": 0,
                "neutral_mentions": 0,
            }

        # Calculate sentiment summary
        sentiment_summary = self._calculate_sentiment_summary(news)

        return {
            "ticker": ticker,
            "sentiment": sentiment_summary["overall"],
            "sentiment_score": sentiment_summary["score"],
            "article_count": len(news),
            "recent_news": news[:5],  # Top 5 articles
            "positive_mentions": sentiment_summary["positive"],
            "negative_mentions": sentiment_summary["negative"],
            "neutral_mentions": sentiment_summary["neutral"],
        }

    def _extract_sentiment(self, article: Dict[str, Any]) -> str:
        """
        Extract sentiment from article data using keyword analysis.

        Args:
            article: Article dictionary with headline and summary

        Returns:
            Sentiment classification: 'positive', 'negative', or 'neutral'
        """
        text = f"{article.get('headline', '')} {article.get('summary', '')}".lower()

        positive_keywords = [
            "surge", "soar", "rally", "gain", "profit", "beat", "upgrade",
            "bullish", "growth", "strong", "outperform", "success", "record",
            "high", "jump", "rise", "climbs", "boost", "positive"
        ]
        negative_keywords = [
            "fall", "drop", "plunge", "loss", "miss", "downgrade", "bearish",
            "decline", "weak", "concern", "risk", "cut", "underperform", "low",
            "tumble", "sink", "crash", "slump", "negative", "disappointing"
        ]

        positive_count = sum(1 for keyword in positive_keywords if keyword in text)
        negative_count = sum(1 for keyword in negative_keywords if keyword in text)

        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        return "neutral"

    def _calculate_sentiment_summary(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate overall sentiment from a list of articles.

        Args:
            articles: List of article dictionaries with sentiment field

        Returns:
            Dictionary with overall sentiment, score, and counts
        """
        if not articles:
            return {
                "overall": "neutral",
                "score": 0.0,
                "positive": 0,
                "negative": 0,
                "neutral": 0
            }

        positive = sum(1 for a in articles if a.get("sentiment") == "positive")
        negative = sum(1 for a in articles if a.get("sentiment") == "negative")
        neutral = sum(1 for a in articles if a.get("sentiment") == "neutral")

        total = len(articles)
        score = (positive - negative) / total if total > 0 else 0.0

        # Determine overall sentiment based on score
        if score > 0.2:
            overall = "positive"
        elif score < -0.2:
            overall = "negative"
        else:
            overall = "neutral"

        return {
            "overall": overall,
            "score": round(score, 2),
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
        }
