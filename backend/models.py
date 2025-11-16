"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class StockQuery(BaseModel):
    """Request model for stock queries."""

    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, TSLA)")
    question: Optional[str] = Field(
        None, description="Specific question about the stock"
    )


class StockInfo(BaseModel):
    """Stock information response."""

    ticker: str
    name: str
    current_price: float
    market_cap: Optional[float]
    pe_ratio: Optional[float]
    dividend_yield: Optional[float]
    fifty_two_week_high: Optional[float]
    fifty_two_week_low: Optional[float]
    volume: Optional[int]
    avg_volume: Optional[int]


class NewsArticle(BaseModel):
    """News article model."""

    title: str
    description: Optional[str]
    url: str
    published_at: str
    source: str


class AnalysisRequest(BaseModel):
    """Request for AI analysis."""

    ticker: str
    stock_data: Dict[str, Any]
    news: List[Dict[str, Any]]
    user_question: Optional[str] = None


class AnalysisResponse(BaseModel):
    """AI analysis response."""

    ticker: str
    analysis: str
    recommendation: Optional[str]
    key_points: List[str]
