#!/usr/bin/env python3
"""Integration tests for stock agent functions."""

import os
import sys
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.stock_agent import extract_ticker, fetch_stock_price, format_stock_response


class TestStockAgentIntegration:
    """Integration tests for stock agent functions."""
    
    @patch('src.agents.stock_agent.yf.Ticker')
    def test_extract_and_fetch_integration(self, mock_ticker_class):
        """Test complete workflow from ticker extraction to price fetching."""
        # Setup mock yfinance response
        mock_ticker = Mock()
        mock_ticker.info = {
            "regularMarketPrice": 250.45,
            "longName": "Tesla, Inc.",
            "currency": "USD"
        }
        mock_ticker_class.return_value = mock_ticker
        
        # Test the complete workflow
        query = "What's the price of Tesla?"
        ticker = extract_ticker(query)
        assert ticker == "TSLA"
        
        stock_data = fetch_stock_price(ticker)
        assert stock_data["ticker"] == "TSLA"
        assert abs(stock_data["price"] - 250.45) < 0.01
        
        formatted_response = format_stock_response(stock_data)
        assert "Tesla, Inc. (TSLA): $250.45 USD" in formatted_response
    
    def test_ticker_extraction_integration(self):
        """Test ticker extraction with various real-world queries."""
        test_cases = [
            ("What is Tesla stock price?", "TSLA"),
            ("How much is Apple worth?", "AAPL"),
            ("NVIDIA current price", "NVDA"),
            ("Show me MSFT", "MSFT"),
            ("Amazon stock today", "AMZN"),
        ]
        
        for query, expected_ticker in test_cases:
            result = extract_ticker(query)
            assert result == expected_ticker, f"Failed for query: {query}"


if __name__ == "__main__":
    print("Running integration tests...")
    import pytest
    pytest.main([__file__])
    print("🎉 All integration tests completed!")