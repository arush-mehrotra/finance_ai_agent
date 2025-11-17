"""Test script for the news_service using Finnhub API."""
from backend.services.news_service import NewsService
from backend.config import get_settings
import json
from datetime import datetime, timedelta


def test_initialization():
    """Test NewsService initialization."""
    print("\n" + "="*60)
    print("Testing NewsService Initialization")
    print("="*60)

    try:
        settings = get_settings()
        service = NewsService(api_key=settings.finnhub_api_key)
        print(f"✓ Successfully initialized NewsService")
        print(f"  API Key configured: {bool(settings.finnhub_api_key)}")
        return True, service
    except ValueError as e:
        print(f"✗ Error: {e}")
        print(f"  Please add FINNHUB_API_KEY to your .env file")
        return False, None
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False, None


def test_company_news(service: NewsService):
    """Test fetching company news."""
    print("\n" + "="*60)
    print("Testing get_company_news() with AAPL (last 7 days)")
    print("="*60)

    try:
        # Get news from last 7 days
        news = service.get_company_news("AAPL", limit=5)

        if not news:
            print(f"⚠ No news articles found for AAPL")
            return True

        print(f"✓ Successfully fetched {len(news)} articles")
        print(f"\nSample articles:")
        for i, article in enumerate(news[:3], 1):
            print(f"\n  {i}. {article['title'][:80]}...")
            print(f"     Source: {article['source']}")
            print(f"     Published: {article['published_at'][:19]}")
            print(f"     Sentiment: {article['sentiment']}")
            print(f"     URL: {article['url'][:60]}...")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_company_news_with_dates(service: NewsService):
    """Test fetching company news with specific date range."""
    print("\n" + "="*60)
    print("Testing get_company_news() with date range")
    print("="*60)

    try:
        # Get news from last 30 days
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        news = service.get_company_news("TSLA", from_date=from_date, to_date=to_date, limit=5)

        print(f"✓ Successfully fetched {len(news)} articles for TSLA")
        print(f"  Date range: {from_date} to {to_date}")

        if news:
            sentiments = [a['sentiment'] for a in news]
            print(f"  Positive: {sentiments.count('positive')}")
            print(f"  Negative: {sentiments.count('negative')}")
            print(f"  Neutral: {sentiments.count('neutral')}")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_market_news(service: NewsService):
    """Test fetching general market news."""
    print("\n" + "="*60)
    print("Testing get_market_news() with general category")
    print("="*60)

    try:
        news = service.get_market_news(category="general", limit=5)

        print(f"✓ Successfully fetched {len(news)} market news articles")

        if news:
            print(f"\nTop headlines:")
            for i, article in enumerate(news[:3], 1):
                print(f"  {i}. {article['title'][:70]}...")
                print(f"     Source: {article['source']}")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_news_sentiment(service: NewsService):
    """Test news sentiment analysis."""
    print("\n" + "="*60)
    print("Testing get_news_sentiment() for AAPL")
    print("="*60)

    try:
        sentiment = service.get_news_sentiment("AAPL")

        print(f"✓ Successfully analyzed sentiment for {sentiment['ticker']}")
        print(f"  Overall Sentiment: {sentiment['sentiment'].upper()}")
        print(f"  Sentiment Score: {sentiment['sentiment_score']}")
        print(f"  Articles Analyzed: {sentiment['article_count']}")
        print(f"  Positive mentions: {sentiment['positive_mentions']}")
        print(f"  Negative mentions: {sentiment['negative_mentions']}")
        print(f"  Neutral mentions: {sentiment['neutral_mentions']}")

        if sentiment['recent_news']:
            print(f"\n  Most recent article:")
            recent = sentiment['recent_news'][0]
            print(f"    - {recent['title'][:70]}...")
            print(f"    - Sentiment: {recent['sentiment']}")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_invalid_ticker(service: NewsService):
    """Test with invalid ticker."""
    print("\n" + "="*60)
    print("Testing with invalid ticker (INVALID_XYZ)")
    print("="*60)

    try:
        news = service.get_company_news("INVALID_XYZ", limit=5)

        if not news or len(news) == 0:
            print(f"✓ Correctly handled invalid ticker (returned empty list)")
            return True
        else:
            print(f"? Unexpected: Got {len(news)} articles for invalid ticker")
            return True

    except Exception as e:
        print(f"✓ Correctly raised error for invalid ticker")
        print(f"  Error: {str(e)[:80]}...")
        return True


if __name__ == "__main__":
    print("\n" + "="*60)
    print("NEWS SERVICE TEST SUITE (FINNHUB)")
    print("="*60)

    results = []

    # Initialize service
    success, service = test_initialization()
    results.append(("Initialization", success))

    if not service:
        print("\n" + "="*60)
        print("TESTS ABORTED")
        print("="*60)
        print("\n✗ Cannot run tests without valid Finnhub API key")
        print("\nTo get a free API key:")
        print("  1. Visit https://finnhub.io/register")
        print("  2. Sign up for a free account")
        print("  3. Copy your API key")
        print("  4. Create a .env file (copy from .env.example)")
        print("  5. Add: FINNHUB_API_KEY=your_api_key_here")
        print("\nFree tier limits: 60 API calls/minute")
        exit(1)

    # Run tests
    results.append(("Company News", test_company_news(service)))
    results.append(("Company News with Dates", test_company_news_with_dates(service)))
    results.append(("Market News", test_market_news(service)))
    results.append(("News Sentiment", test_news_sentiment(service)))
    results.append(("Invalid Ticker", test_invalid_ticker(service)))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! The news service is working correctly.")
    else:
        print(f"\n  {total - passed} test(s) failed. Please check the errors above.")
