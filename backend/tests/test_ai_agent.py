"""Test script for the AI agent and portfolio analyzer services."""
from backend.services.ai_agent import AIAgentService
from backend.services.portfolio_analyzer import PortfolioAnalyzer
from backend.services.stock_data import StockDataService
from backend.services.news_service import NewsService
from backend.config import get_settings


def test_ai_agent_initialization():
    """Test AI agent initialization."""
    print("\n" + "="*60)
    print("Testing AI Agent Initialization")
    print("="*60)

    try:
        settings = get_settings()
        agent = AIAgentService(api_key=settings.anthropic_api_key)
        print(f"✓ Successfully initialized AI Agent")
        print(f"  Model: {agent.model}")
        print(f"  API Key configured: {bool(settings.anthropic_api_key)}")
        return True, agent
    except ValueError as e:
        print(f"✗ Error: {e}")
        print(f"  Please add ANTHROPIC_API_KEY to your .env file")
        return False, None
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False, None


def test_stock_analysis(agent: AIAgentService):
    """Test AI stock analysis."""
    print("\n" + "="*60)
    print("Testing AI Stock Analysis for AAPL")
    print("="*60)

    try:
        # Get real stock data
        stock_service = StockDataService()
        stock_data = stock_service.get_stock_info("AAPL")

        # Get news
        settings = get_settings()
        news_service = NewsService(api_key=settings.finnhub_api_key)
        news = news_service.get_company_news("AAPL", limit=5)

        print(f"  Fetched data for {stock_data['name']}")
        print(f"  Current price: ${stock_data['current_price']}")
        print(f"  News articles: {len(news)}")

        # Generate AI analysis
        print(f"\n  Generating AI analysis... (this may take a few seconds)")
        analysis = agent.analyze_stock("AAPL", stock_data, news)

        print(f"\n✓ Successfully generated analysis")
        print(f"\n  Analysis Preview:")
        print(f"  {analysis['analysis'][:200]}...")
        print(f"\n  Key Points:")
        for i, point in enumerate(analysis['key_points'][:3], 1):
            print(f"    {i}. {point}")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_answer_question(agent: AIAgentService):
    """Test answering specific questions."""
    print("\n" + "="*60)
    print("Testing Question Answering")
    print("="*60)

    try:
        # Get stock data
        stock_service = StockDataService()
        stock_data = stock_service.get_stock_info("TSLA")

        # Get news
        settings = get_settings()
        news_service = NewsService(api_key=settings.finnhub_api_key)
        news = news_service.get_company_news("TSLA", limit=3)

        question = "Is this stock overvalued based on its P/E ratio?"
        print(f"  Question: {question}")
        print(f"  Generating answer... (this may take a few seconds)")

        answer = agent.answer_question("TSLA", question, stock_data, news)

        print(f"\n✓ Successfully generated answer")
        print(f"\n  Answer:")
        print(f"  {answer[:300]}...")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_news_summarization(agent: AIAgentService):
    """Test news summarization."""
    print("\n" + "="*60)
    print("Testing News Summarization")
    print("="*60)

    try:
        # Get news
        settings = get_settings()
        news_service = NewsService(api_key=settings.finnhub_api_key)
        news = news_service.get_company_news("MSFT", limit=5)

        print(f"  Summarizing {len(news)} news articles for MSFT...")

        summary = agent.summarize_news("MSFT", news)

        print(f"\n✓ Successfully summarized news")
        print(f"\n  Summary: {summary['summary']}")
        print(f"  Sentiment: {summary['sentiment'].upper()}")
        print(f"  Key Points:")
        for i, point in enumerate(summary['key_points'], 1):
            print(f"    {i}. {point}")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_portfolio_analyzer():
    """Test the integrated portfolio analyzer."""
    print("\n" + "="*60)
    print("Testing Portfolio Analyzer (Full Integration)")
    print("="*60)

    try:
        settings = get_settings()
        analyzer = PortfolioAnalyzer(
            anthropic_api_key=settings.anthropic_api_key,
            finnhub_api_key=settings.finnhub_api_key
        )

        print(f"  Running comprehensive analysis for AAPL...")
        print(f"  (this may take 10-15 seconds)")

        result = analyzer.analyze_investment("AAPL", include_recommendation=True)

        if not result['success']:
            print(f"✗ Analysis failed: {result.get('error')}")
            return False

        print(f"\n✓ Successfully completed comprehensive analysis")
        print(f"\n  Stock: {result['stock_info']['name']}")
        print(f"  Price: ${result['stock_info']['current_price']}")
        print(f"  P/E Ratio: {result['stock_info']['pe_ratio']}")
        print(f"  News Sentiment: {result['news_summary']['sentiment'].upper()}")

        if result['recommendation']:
            print(f"\n  Recommendation: {result['recommendation']['recommendation']}")
            print(f"  Confidence: {result['recommendation']['confidence']}")
            print(f"  Reasoning: {result['recommendation']['reasoning'][:150]}...")

        print(f"\n  AI Analysis Preview:")
        print(f"  {result['ai_analysis']['analysis'][:250]}...")

        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("AI AGENT & PORTFOLIO ANALYZER TEST SUITE")
    print("="*60)

    results = []

    # Initialize AI agent
    success, agent = test_ai_agent_initialization()
    results.append(("AI Agent Initialization", success))

    if not agent:
        print("\n" + "="*60)
        print("TESTS ABORTED")
        print("="*60)
        print("\n✗ Cannot run tests without valid Anthropic API key")
        print("\nTo get an API key:")
        print("  1. Visit https://console.anthropic.com")
        print("  2. Sign up and navigate to API Keys")
        print("  3. Create a new key")
        print("  4. Add to .env file: ANTHROPIC_API_KEY=your_key_here")
        print("\nNote: You also need FINNHUB_API_KEY for full functionality")
        exit(1)

    # Run AI agent tests
    print("\n" + "-"*60)
    print("Running AI Agent Tests")
    print("-"*60)

    results.append(("Stock Analysis", test_stock_analysis(agent)))
    results.append(("Question Answering", test_answer_question(agent)))
    results.append(("News Summarization", test_news_summarization(agent)))

    # Run integration test
    print("\n" + "-"*60)
    print("Running Integration Tests")
    print("-"*60)

    results.append(("Portfolio Analyzer", test_portfolio_analyzer()))

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
        print("\n🎉 All tests passed! The AI agent is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")

    print("\n" + "="*60)
    print("COST ESTIMATE")
    print("="*60)
    print("This test suite made approximately 4-5 API calls to Claude.")
    print("Estimated cost: $0.01 - $0.03 USD")
    print("(Based on Claude Sonnet pricing)")
