"""AI analysis API routes."""
from fastapi import APIRouter, HTTPException, Body
from typing import Optional, List
from pydantic import BaseModel
from backend.services.portfolio_analyzer import PortfolioAnalyzer
from backend.config import get_settings

router = APIRouter()


# Request models
class AnalysisRequest(BaseModel):
    """Request model for investment analysis."""
    ticker: str
    question: Optional[str] = None
    include_recommendation: bool = True


class QuestionRequest(BaseModel):
    """Request model for Q&A."""
    ticker: str
    question: str


class CompareRequest(BaseModel):
    """Request model for stock comparison."""
    tickers: List[str]


def get_portfolio_analyzer():
    """Get portfolio analyzer instance with API keys from settings."""
    settings = get_settings()
    return PortfolioAnalyzer(
        anthropic_api_key=settings.anthropic_api_key,
        finnhub_api_key=settings.finnhub_api_key,
        ai_model=settings.ai_model
    )


@router.post("/analyze")
async def analyze_investment(request: AnalysisRequest):
    """
    Perform comprehensive AI-powered investment analysis.

    Returns stock data, news sentiment, AI analysis, and recommendation.

    **Example request:**
    ```json
    {
        "ticker": "AAPL",
        "question": "Is this a good long-term investment?",
        "include_recommendation": true
    }
    ```
    """
    try:
        analyzer = get_portfolio_analyzer()

        result = analyzer.analyze_investment(
            ticker=request.ticker.upper(),
            user_question=request.question,
            include_recommendation=request.include_recommendation
        )

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Analysis failed"))

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Ask a specific question about a stock.

    Get AI-powered answers based on current stock data and news.

    **Example request:**
    ```json
    {
        "ticker": "TSLA",
        "question": "Is this stock overvalued?"
    }
    ```
    """
    try:
        analyzer = get_portfolio_analyzer()

        result = analyzer.answer_question(
            ticker=request.ticker.upper(),
            question=request.question
        )

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to answer question"))

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare")
async def compare_stocks(request: CompareRequest):
    """
    Compare multiple stocks side by side.

    Returns key metrics for each stock.

    **Example request:**
    ```json
    {
        "tickers": ["AAPL", "GOOGL", "MSFT"]
    }
    ```
    """
    try:
        if len(request.tickers) < 2:
            raise HTTPException(status_code=400, detail="At least 2 tickers required for comparison")

        if len(request.tickers) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 tickers allowed")

        analyzer = get_portfolio_analyzer()
        tickers = [t.upper() for t in request.tickers]

        result = analyzer.compare_stocks(tickers)

        return {
            "success": True,
            "data": result
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyze/{ticker}/news-summary")
async def get_news_summary(ticker: str):
    """
    Get AI-powered news summary for a stock.

    Returns summarized news with key insights.
    """
    try:
        analyzer = get_portfolio_analyzer()

        result = analyzer.get_news_summary(ticker.upper())

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to generate summary"))

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
