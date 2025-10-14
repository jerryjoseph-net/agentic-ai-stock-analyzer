"""Unit tests for stock agent functions using TDD approach."""
import pytest
from unittest.mock import Mock, patch

from src.agents.stock_agent import extract_ticker, fetch_stock_price, format_stock_response, validate_ticker


class TestStockAgentFunctions:
    """Test cases for stock agent functions following TDD principles."""
    
    # Test extract_ticker function
    @pytest.mark.parametrize("query,expected_ticker", [
        ("What's the price of Tesla?", "TSLA"),
        ("How much is Apple stock?", "AAPL"),
        ("NVIDIA price", "NVDA"),
        ("Microsoft today", "MSFT"),
        ("Amazon stock", "AMZN"),
        ("Google share price", "GOOGL"),
        ("Meta stock price", "META"),
        ("Tell me about TSLA", "TSLA"),
        ("Show me AAPL", "AAPL"),
        ("", "UNKNOWN"),
        ("What's the weather?", "UNKNOWN"),
        ("Random text", "UNKNOWN"),
    ])
    def test_extract_ticker_various_queries(self, query, expected_ticker):
        """Test ticker extraction from various query formats."""
        result = extract_ticker(query)
        assert result == expected_ticker

    def test_extract_ticker_case_insensitive(self):
        """Test that ticker extraction is case insensitive for company names."""
        assert extract_ticker("tesla stock") == "TSLA"
        assert extract_ticker("TESLA stock") == "TSLA"
        assert extract_ticker("Tesla stock") == "TSLA"

    def test_extract_ticker_direct_symbols(self):
        """Test extraction of direct ticker symbols."""
        assert extract_ticker("AAPL") == "AAPL"
        assert extract_ticker("Check MSFT today") == "MSFT"
        assert extract_ticker("GOOGL and AMZN") == "GOOGL"  # First match

    # Test validate_ticker function
    @pytest.mark.parametrize("ticker,expected_valid", [
        ("TSLA", True),
        ("AAPL", True),
        ("MSFT", True),
        ("A", True),
        ("GOOGL", True),
        ("", False),
        ("UNKNOWN", False),
        ("123", False),
        ("TOOLONG", False),  # More than 5 chars
        ("tsla", False),     # Lowercase
        ("TS-LA", False),    # Invalid chars
    ])
    def test_validate_ticker_formats(self, ticker, expected_valid):
        """Test ticker validation for various formats."""
        result = validate_ticker(ticker)
        assert result == expected_valid

    # Test fetch_stock_price function
    @patch('src.agents.stock_agent.yf.Ticker')
    def test_fetch_stock_price_success(self, mock_ticker_class):
        """Test successful stock price fetching."""
        # Setup mock yfinance response
        mock_ticker = Mock()
        mock_ticker.info = {
            "regularMarketPrice": 250.45,
            "longName": "Tesla, Inc.",
            "currency": "USD"
        }
        mock_ticker_class.return_value = mock_ticker
        
        result = fetch_stock_price("TSLA")
        
        assert result["ticker"] == "TSLA"
        assert result["company_name"] == "Tesla, Inc."
        assert result["price"] == 250.45
        assert result["currency"] == "USD"
        assert "timestamp" in result
        assert result["change"] == "+0.00%"

    @patch('src.agents.stock_agent.yf.Ticker')
    def test_fetch_stock_price_fallback_to_history(self, mock_ticker_class):
        """Test fallback to history when regularMarketPrice not available."""
        # Setup mock for fallback scenario
        mock_ticker = Mock()
        mock_ticker.info = {}  # No regularMarketPrice
        
        # Mock history data
        import pandas as pd
        mock_history = pd.DataFrame({'Close': [245.67]})
        mock_ticker.history.return_value = mock_history
        mock_ticker_class.return_value = mock_ticker
        
        result = fetch_stock_price("TSLA")
        
        assert result["ticker"] == "TSLA"
        assert result["price"] == 245.67

    @patch('src.agents.stock_agent.yf.Ticker')
    def test_fetch_stock_price_invalid_ticker(self, mock_ticker_class):
        """Test handling of invalid ticker symbols."""
        from src.utils.exceptions import StockNotFoundError
        
        # Setup mock for invalid ticker
        mock_ticker = Mock()
        mock_ticker.info = {}
        import pandas as pd
        mock_ticker.history.return_value = pd.DataFrame()  # Empty history
        mock_ticker_class.return_value = mock_ticker
        
        with pytest.raises(StockNotFoundError):
            fetch_stock_price("INVALID")

    def test_fetch_stock_price_invalid_format(self):
        """Test rejection of invalid ticker formats."""
        from src.utils.exceptions import StockNotFoundError
        
        with pytest.raises(StockNotFoundError):
            fetch_stock_price("invalid")
        
        with pytest.raises(StockNotFoundError):
            fetch_stock_price("")

    # Test format_stock_response function
    def test_format_stock_response_complete_data(self):
        """Test formatting with complete stock data."""
        stock_data = {
            "ticker": "TSLA",
            "company_name": "Tesla, Inc.",
            "price": 250.45,
            "currency": "USD",
            "change": "+2.15%"
        }
        
        result = format_stock_response(stock_data)
        expected = "Tesla, Inc. (TSLA): $250.45 USD (+2.15%)"
        assert result == expected

    def test_format_stock_response_minimal_data(self):
        """Test formatting with minimal stock data."""
        stock_data = {
            "ticker": "AAPL",
            "company_name": "Apple Inc.",
            "price": 175.50,
            "currency": "USD",
            "change": "+0.00%"
        }
        
        result = format_stock_response(stock_data)
        expected = "Apple Inc. (AAPL): $175.50 USD (+0.00%)"
        assert result == expected

    def test_format_stock_response_decimal_precision(self):
        """Test that price formatting shows proper decimal precision."""
        stock_data = {
            "ticker": "MSFT",
            "company_name": "Microsoft Corporation",
            "price": 299.999,
            "currency": "USD",
            "change": "+1.23%"
        }
        
        result = format_stock_response(stock_data)
        expected = "Microsoft Corporation (MSFT): $300.00 USD (+1.23%)"
        assert result == expected

