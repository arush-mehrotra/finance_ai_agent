"""News API routes."""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime, timedelta
from backend.services.news_service import NewsService
from backend.config import get_settings

router = APIRouter()


def get_news_service():
    """Get news service instance with API key from settings."""
    settings = get_settings()
    return NewsService(api_key=settings.finnhub_api_key)


@router.get("/news/{ticker}")
async def get_company_news(
    ticker: str,
    from_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    to_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    limit: int = Query(20, ge=1, le=50, description="Number of articles (1-50)")
):
    """
    Get news articles for a specific company.

    Returns recent news with sentiment analysis.
    """
    try:
        news_service = get_news_service()

        # Set default dates if not provided
        if not to_date:
            to_date = datetime.now().strftime("%Y-%m-%d")
        if not from_date:
            from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        news = news_service.get_company_news(
            ticker=ticker.upper(),
            from_date=from_date,
            to_date=to_date,
            limit=limit
        )

        return {
            "success": True,
            "data": news,
            "count": len(news),
            "ticker": ticker.upper(),
            "date_range": {
                "from": from_date,
                "to": to_date
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/news/market")
async def get_market_news(
    category: str = Query("general", description="News category (general, forex, crypto, merger)"),
    limit: int = Query(20, ge=1, le=50, description="Number of articles (1-50)")
):
    """
    Get general market news.

    Categories: general, forex, crypto, merger
    """
    try:
        news_service = get_news_service()
        news = news_service.get_market_news(category=category, limit=limit)

        return {
            "success": True,
            "data": news,
            "count": len(news),
            "category": category
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/news/{ticker}/sentiment")
async def get_news_sentiment(ticker: str):
    """
    Get news sentiment analysis for a ticker.

    Returns overall sentiment, score, and recent articles.
    """
    try:
        news_service = get_news_service()
        sentiment = news_service.get_news_sentiment(ticker.upper())

        return {
            "success": True,
            "data": sentiment
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
