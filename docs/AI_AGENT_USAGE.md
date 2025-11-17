# AI Agent Usage Guide

## Quick Start

```python
from backend.services.portfolio_analyzer import PortfolioAnalyzer

# Initialize
analyzer = PortfolioAnalyzer(
    anthropic_api_key="your_key",
    finnhub_api_key="your_key"
)

# Complete analysis with recommendation
result = analyzer.analyze_investment("AAPL", include_recommendation=True)
print(result['ai_analysis']['analysis'])
print(result['recommendation']['recommendation'])  # BUY/HOLD/SELL

# Ask specific questions
answer = analyzer.answer_question("TSLA", "Is this overvalued?")
print(answer['answer'])

# Compare stocks
comparison = analyzer.compare_stocks(["AAPL", "GOOGL", "MSFT"])
```

---

## Available Functions

### Portfolio Analyzer (Main Interface)
- `analyze_investment(ticker, question?, include_recommendation?)` - Full stock analysis
- `answer_question(ticker, question)` - Answer specific questions
- `compare_stocks(tickers[])` - Compare multiple stocks
- `get_news_summary(ticker)` - AI news summary

### AI Agent (Direct Access)
- `analyze_stock(ticker, stock_data, news)` - Generate analysis
- `answer_question(ticker, question, stock_data, news)` - Q&A
- `summarize_news(ticker, news)` - Summarize news
- `generate_recommendation(ticker, analysis, stock_data)` - Buy/hold/sell

---

## Configuration (Optional)

Add to `.env`:
```bash
AI_MODEL=claude-sonnet-4-5-20250929  # default
AI_TEMPERATURE=0.7                    # default
AI_MAX_TOKENS=2048                    # default
```

---

## Testing

```bash
./run_tests.sh ai      # Test AI agent only
./run_tests.sh all     # Test everything
```

---

## Cost Estimate

**Typical usage:**
- Single analysis: ~$0.01
- 100 analyses/month: ~$1.00

Monitor usage at https://console.anthropic.com
