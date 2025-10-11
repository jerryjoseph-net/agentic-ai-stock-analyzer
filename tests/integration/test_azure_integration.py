#!/usr/bin/env python3
"""Test the complete Azure OpenAI integration workflow - Public API only."""

import pytest
import asyncio
import sys
import os
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


# Mock classes for testing
class MockResponse:
    """Mock response object that works with agent framework expectations."""
    def __init__(self, ticker="TSLA"):
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


def test_complete_workflow():
    """Test the complete StockAgent workflow with Azure OpenAI - Public API only."""
    from src.agents.stock_agent import StockAgent

    print("🔧 Setting up test with mocked Azure OpenAI...")
    
    agent = StockAgent()
    agent.chat_client = MockChatClient("TSLA")
    print("✅ StockAgent created successfully")

    # Test complete workflow through run method
    query = "What's the price of Tesla stock?"
    print(f"🔧 Testing complete workflow with query: '{query}'")
    
    # Mock yfinance for stock price fetching
    with patch('src.agents.stock_agent.yf.Ticker') as mock_yf_ticker:
        mock_ticker_instance = Mock()
        mock_ticker_instance.info = {
            "regularMarketPrice": 184.50,
            "longName": "Tesla, Inc.",
            "currency": "USD"
        }
        mock_yf_ticker.return_value = mock_ticker_instance
        
        result = asyncio.run(agent.run(query))
        print(f"✅ Complete workflow result: {result}")
        
        # Verify the response
        assert result.response_id == "stock-info-TSLA"
        assert len(result.messages) > 0
        response_text = result.messages[0].text
        assert "Tesla, Inc." in response_text
        assert "$184.50" in response_text
        assert "TSLA" in response_text
        
    print("✅ Complete workflow test passed!")


@pytest.mark.asyncio
async def test_stock_agent_basic():
    """Test that StockAgent can be instantiated and run method works."""
    from src.utils.config import AgentConfig
    from src.agents.stock_agent import StockAgent

    config = AgentConfig(
        azure_ai_endpoint="https://test.openai.azure.com/",
        azure_ai_api_key="test-key",
        azure_ai_api_version="2024-12-01-preview",
        azure_ai_model_deployment="o3-mini"
    )

    with patch('src.agents.stock_agent.AzureOpenAIChatClient') as mock_azure_client:
        mock_chat_client = MockChatClient("TSLA")
        mock_azure_client.return_value = mock_chat_client
        
        agent = StockAgent(config=config)
        
        # Mock yfinance for complete workflow
        with patch('src.agents.stock_agent.yf.Ticker') as mock_yf_ticker:
            mock_ticker_instance = Mock()
            mock_ticker_instance.info = {
                "regularMarketPrice": 250.45,
                "longName": "Tesla Inc",
                "currency": "USD"
            }
            mock_yf_ticker.return_value = mock_ticker_instance
            
            result = await agent.run("What's the price of Tesla?")
            assert result.response_id == "stock-info-TSLA"
            assert "Tesla Inc" in result.messages[0].text


def test_error_handling():
    """Test error handling in the StockAgent - Public API only."""
    from src.agents.stock_agent import StockAgent
    
    print("🔧 Testing error handling...")
    
    # Test empty query
    with patch('agents.stock_agent.AzureOpenAIChatClient') as mock_azure_client:
        mock_chat_client = MockChatClient("TSLA")
        mock_azure_client.return_value = mock_chat_client
        agent = StockAgent()
        
        result = asyncio.run(agent.run(""))
        assert result.response_id == "no-query"
        assert result.messages == []
        print("✅ Empty query handled correctly")
            
        # Test Azure OpenAI API error by making the mock agent raise an exception
        class ErrorAgent:
            async def run(self, query):
                raise Exception("API Error")
        
        class ErrorChatClient:
            def create_agent(self, **kwargs):
                return ErrorAgent()
        
        # Create agent first, then override its chat_client
        agent = StockAgent()
        agent.chat_client = ErrorChatClient()
        
        result = asyncio.run(agent.run("What's Tesla's price?"))
        assert result.response_id == "error"
        assert "couldn't process" in result.messages[0].text.lower()
        print("✅ API error handled correctly")


if __name__ == "__main__":
    print("🚀 Starting Azure OpenAI integration tests...\n")
    test_complete_workflow()
    print("\n")
    asyncio.run(test_stock_agent_basic())
    print("\n")
    test_error_handling()
    print("\n🎉 All Azure integration tests passed!")