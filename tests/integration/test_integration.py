#!/usr/bin/env python3
"""Simple integration tes        with patch('src.agents.stock_agent.AzureOpenAIChatClient') as mock_azure_client: for StockAgent with Azure OpenAI."""

import os
import sys
from unittest.mock import Mock, patch, AsyncMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.stock_agent import StockAgent
from src.utils.config import AgentConfig


class MockResponse:
    """Mock response object that works with agent framework expectations."""
    def __init__(self, ticker):
        self.response_id = ticker
        self.messages = []  # Empty messages list to trigger fallback to response_id


class MockAgent:
    """Mock agent that returns MockResponse."""
    def __init__(self, ticker="TSLA"):
        self.ticker = ticker
    
    async def run(self, query):
        return MockResponse(self.ticker)


class MockChatClient:
    """Mock chat client that returns MockAgent."""
    def __init__(self, ticker="TSLA"):
        self.ticker = ticker
    
    def create_agent(self, **kwargs):
        return MockAgent(self.ticker)

def test_stock_agent_basic():
    """Test that StockAgent can be instantiated and basic methods work."""
    # Create test config
    config = AgentConfig(
        azure_ai_endpoint="https://test.openai.azure.com/",
        azure_ai_api_key="test-key",
        azure_ai_api_version="2024-12-01-preview",
        azure_ai_model_deployment="o3-mini"
    )
    
    # Mock Azure OpenAI client using MockChatClient
    with patch('src.agents.stock_agent.AzureOpenAIChatClient') as mock_azure_client:
        mock_chat_client = MockChatClient("TSLA")
        mock_azure_client.return_value = mock_chat_client
        
        # Create agent
        agent = StockAgent(config=config)
        
        # Test complete workflow through run method
        import asyncio
        result = asyncio.run(agent.run("What's the price of Tesla?"))
        assert result.response_id.startswith("stock-info")
        assert len(result.messages) > 0
        
        # Verify Azure OpenAI client was called correctly
        mock_azure_client.assert_called_once_with(
            endpoint=config.azure_ai_endpoint,
            api_key=config.azure_ai_api_key,
            api_version=config.azure_ai_api_version,
            deployment_name=config.azure_ai_model_deployment
        )
        
        print("✅ Stock agent basic functionality test passed!")

def test_stock_price_fetching():
    """Test stock price fetching with mocked yfinance - complete workflow."""
    config = AgentConfig(
        azure_ai_endpoint="https://test.openai.azure.com/",
        azure_ai_api_key="test-key"
    )
    
    with patch('src.agents.stock_agent.AzureOpenAIChatClient') as mock_azure_client:
        mock_chat_client = MockChatClient("TSLA")
        mock_azure_client.return_value = mock_chat_client
        
        agent = StockAgent(config=config)
        
        # Mock yfinance and test complete workflow
        with patch('src.agents.stock_agent.yf.Ticker') as mock_ticker:
            mock_ticker_instance = Mock()
            mock_ticker_instance.info = {
                "regularMarketPrice": 150.50,
                "longName": "Tesla Inc",
                "currency": "USD"
            }
            mock_ticker.return_value = mock_ticker_instance
            
            # Test complete workflow through run method
            import asyncio
            result = asyncio.run(agent.run("What's the price of Tesla?"))
            
            assert result.response_id.startswith("stock-info")
            assert len(result.messages) > 0
            assert "Tesla Inc" in result.messages[0].text
            assert "150.50" in result.messages[0].text
            
            print("✅ Stock price fetching test passed!")

if __name__ == "__main__":
    print("Running integration tests...")
    test_stock_agent_basic()
    test_stock_price_fetching()
    print("🎉 All integration tests passed!")