"""Simple test script to verify the stock_data service is working."""
from backend.services.stock_data import StockDataService
import json


def test_stock_info():
    """Test fetching stock info."""
    print("\n" + "="*60)
    print("Testing get_stock_info() with AAPL")
    print("="*60)
    
    try:
        info = StockDataService.get_stock_info("AAPL")
        print(f"✓ Successfully fetched data for {info['name']}")
        print(f"  Ticker: {info['ticker']}")
        print(f"  Current Price: ${info['current_price']}")
        print(f"  Market Cap: ${info['market_cap']:,}" if info['market_cap'] else "  Market Cap: N/A")
        print(f"  P/E Ratio: {info['pe_ratio']}")
        print(f"  Sector: {info['sector']}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_historical_data():
    """Test fetching historical data."""
    print("\n" + "="*60)
    print("Testing get_historical_data() with AAPL (last 5 days)")
    print("="*60)
    
    try:
        hist = StockDataService.get_historical_data("AAPL", period="5d")
        print(f"✓ Successfully fetched {len(hist)} days of data")
        print(f"  Date range: {hist.index[0].date()} to {hist.index[-1].date()}")
        print(f"  Latest close: ${hist['Close'].iloc[-1]:.2f}")
        print(f"  Columns: {', '.join(hist.columns)}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_price_summary():
    """Test price summary."""
    print("\n" + "="*60)
    print("Testing get_price_summary() with AAPL")
    print("="*60)
    
    try:
        summary = StockDataService.get_price_summary("AAPL", period="1mo")
        if "error" in summary:
            print(f"✗ Error: {summary['error']}")
            return False
        
        print(f"✓ Successfully fetched price summary")
        print(f"  Current Price: ${summary['current_price']}")
        print(f"  Period Return: {summary['period_return_pct']}%")
        print(f"  Period High: ${summary['period_high']}")
        print(f"  Period Low: ${summary['period_low']}")
        print(f"  Volatility: {summary['volatility']}%")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_financial_metrics():
    """Test financial metrics."""
    print("\n" + "="*60)
    print("Testing get_financial_metrics() with AAPL")
    print("="*60)
    
    try:
        metrics = StockDataService.get_financial_metrics("AAPL")
        if "error" in metrics:
            print(f"✗ Error: {metrics['error']}")
            return False
        
        print(f"✓ Successfully fetched financial metrics")
        print(f"  Valuation metrics: {len([k for k, v in metrics['valuation'].items() if v is not None])} available")
        print(f"  Profitability metrics: {len([k for k, v in metrics['profitability'].items() if v is not None])} available")
        print(f"  Growth metrics: {len([k for k, v in metrics['growth'].items() if v is not None])} available")
        print(f"  Financial health metrics: {len([k for k, v in metrics['financial_health'].items() if v is not None])} available")
        
        # Show some sample values
        if metrics['valuation']['pe_ratio']:
            print(f"    - P/E Ratio: {metrics['valuation']['pe_ratio']:.2f}")
        if metrics['profitability']['profit_margins']:
            print(f"    - Profit Margin: {metrics['profitability']['profit_margins']*100:.2f}%")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("STOCK DATA SERVICE TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run all tests
    results.append(("Stock Info", test_stock_info()))
    results.append(("Historical Data", test_historical_data()))
    results.append(("Price Summary", test_price_summary()))
    results.append(("Financial Metrics", test_financial_metrics()))
    
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
        print("\n🎉 All tests passed! The stock_data service is working correctly.")
    else:
        print(f"\n  {total - passed} test(s) failed. Please check the errors above.")

