"""
Live Azure integration test (no mocking).
This test will make real calls to test the function-based approach.
Run only when you want to verify real connectivity and API response.
"""
import pytest
from src.agents.stock_agent import extract_ticker, fetch_stock_price, format_stock_response
from src.utils.exceptions import StockNotFoundError

@pytest.mark.live
def test_real_stock_price_fetching():
    """Test real stock price fetching with yfinance."""
    try:
        # Test with known ticker
        stock_data = fetch_stock_price("TSLA")
        assert stock_data["ticker"] == "TSLA"
        assert "Tesla" in stock_data["company_name"]
        assert stock_data["price"] > 0
        assert stock_data["currency"] == "USD"
        print(f"Real Tesla price: {stock_data['price']}")
    except StockNotFoundError as e:
        pytest.fail(f"Stock fetching failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

@pytest.mark.live  
def test_ticker_extraction_real():
    """Test ticker extraction with real queries."""
    queries = [
        ("What's Tesla stock price?", "TSLA"),
        ("Apple stock", "AAPL"), 
        ("Microsoft price", "MSFT")
    ]
    
    for query, expected in queries:
        result = extract_ticker(query)
        assert result == expected, f"Failed for '{query}': got {result}, expected {expected}"
