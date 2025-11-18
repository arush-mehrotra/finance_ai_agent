# Finance AI Agent API Documentation

## Quick Start

### Start the Server
```bash
./start_server.sh
```

Server runs on: **http://localhost:8000**

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Endpoints

### Health Check

**GET /** or **GET /health**
```bash
curl http://localhost:8000/health
```

---

### Stock Data

**GET /api/stock/{ticker}** - Get stock info
```bash
curl http://localhost:8000/api/stock/AAPL
```

**GET /api/stock/{ticker}/history** - Historical data
```bash
curl "http://localhost:8000/api/stock/AAPL/history?period=1mo&interval=1d"
```

**GET /api/stock/{ticker}/metrics** - Financial metrics
```bash
curl http://localhost:8000/api/stock/AAPL/metrics
```

**GET /api/stock/{ticker}/summary** - Price summary
```bash
curl "http://localhost:8000/api/stock/AAPL/summary?period=1y"
```

---

### News

**GET /api/news/{ticker}** - Company news
```bash
curl "http://localhost:8000/api/news/AAPL?limit=10"
```

**GET /api/news/market** - Market news
```bash
curl "http://localhost:8000/api/news/market?category=general&limit=20"
```

**GET /api/news/{ticker}/sentiment** - News sentiment
```bash
curl http://localhost:8000/api/news/AAPL/sentiment
```

---

### AI Analysis

**POST /api/analyze** - Full investment analysis
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "question": "Is this a good long-term investment?",
    "include_recommendation": true
  }'
```

**POST /api/ask** - Ask questions
```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "TSLA",
    "question": "Is this stock overvalued?"
  }'
```

**POST /api/compare** - Compare stocks
```bash
curl -X POST http://localhost:8000/api/compare \
  -H "Content-Type: application/json" \
  -d '{
    "tickers": ["AAPL", "GOOGL", "MSFT"]
  }'
```

**GET /api/analyze/{ticker}/news-summary** - AI news summary
```bash
curl http://localhost:8000/api/analyze/AAPL/news-summary
```

---

## Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "error": "Error Type",
  "detail": "Error message"
}
```

---

## Example Usage (Python)

```python
import requests

# Get stock info
response = requests.get("http://localhost:8000/api/stock/AAPL")
data = response.json()
print(data['data']['current_price'])

# AI analysis
response = requests.post(
    "http://localhost:8000/api/analyze",
    json={
        "ticker": "AAPL",
        "include_recommendation": True
    }
)
result = response.json()
print(result['recommendation']['recommendation'])  # BUY/HOLD/SELL
```

---

## Example Usage (JavaScript)

```javascript
// Get stock info
fetch('http://localhost:8000/api/stock/AAPL')
  .then(res => res.json())
  .then(data => console.log(data.data.current_price));

// AI analysis
fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    ticker: 'AAPL',
    include_recommendation: true
  })
})
  .then(res => res.json())
  .then(data => console.log(data.recommendation));
```

---

## Rate Limits

- **Finnhub (News):** 60 calls/minute (free tier)
- **Anthropic (AI):** 50 requests/minute
- **Yahoo Finance (Stock Data):** No official limit

---

## Notes

- All ticker symbols are automatically converted to uppercase
- Dates should be in YYYY-MM-DD format
- Historical data periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max
- News categories: general, forex, crypto, merger
