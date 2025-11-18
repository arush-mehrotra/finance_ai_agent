"""Stock data API routes."""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from backend.services.stock_data import StockDataService

router = APIRouter()
stock_service = StockDataService()


@router.get("/stock/{ticker}")
async def get_stock_info(ticker: str):
    """
    Get comprehensive stock information.

    Returns basic info, valuation metrics, and fundamentals.
    """
    try:
        info = stock_service.get_stock_info(ticker.upper())
        return {
            "success": True,
            "data": info
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stock/{ticker}/history")
async def get_stock_history(
    ticker: str,
    period: str = Query("1mo", description="Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)"),
    interval: str = Query("1d", description="Data interval (1m, 5m, 1h, 1d, 1wk, 1mo)")
):
    """
    Get historical price data.

    Returns OHLCV (Open, High, Low, Close, Volume) data.
    """
    try:
        hist = stock_service.get_historical_data(ticker.upper(), period=period, interval=interval)

        # Convert DataFrame to JSON-serializable format
        if hist.empty:
            return {
                "success": True,
                "data": [],
                "message": "No historical data available"
            }

        hist_data = hist.reset_index().to_dict(orient="records")
        # Convert Timestamp to string
        for record in hist_data:
            if 'Date' in record:
                record['Date'] = record['Date'].isoformat()

        return {
            "success": True,
            "data": hist_data,
            "period": period,
            "interval": interval
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stock/{ticker}/metrics")
async def get_financial_metrics(ticker: str):
    """
    Get detailed financial metrics.

    Returns valuation, profitability, growth, and financial health metrics.
    """
    try:
        metrics = stock_service.get_financial_metrics(ticker.upper())

        if "error" in metrics:
            raise HTTPException(status_code=400, detail=metrics["error"])

        return {
            "success": True,
            "data": metrics
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stock/{ticker}/summary")
async def get_price_summary(
    ticker: str,
    period: str = Query("1y", description="Time period for analysis")
):
    """
    Get price summary statistics.

    Returns current price, period returns, highs/lows, and volatility.
    """
    try:
        summary = stock_service.get_price_summary(ticker.upper(), period=period)

        if "error" in summary:
            raise HTTPException(status_code=400, detail=summary["error"])

        return {
            "success": True,
            "data": summary,
            "period": period
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
