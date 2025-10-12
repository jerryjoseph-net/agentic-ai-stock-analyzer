"""Unit tests for StockAgent using TDD approach - Public API only."""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.agents.stock_agent import StockAgent
from src.utils.exceptions import StockNotFoundError, APIRateLimitError, AgentError


class TestStockAgent:
    """Test cases for StockAgent following TDD principles - Testing only public API."""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing."""
        from src.utils.config import AgentConfig
        return AgentConfig(
            azure_ai_endpoint="https://test.openai.azure.com/",
            azure_ai_api_key="test-key",
            azure_ai_api_version="2024-12-01-preview",
            azure_ai_model_deployment="o3-mini"
        )
    
    @pytest.fixture
    def mock_azure_client(self):
        """Mock Azure OpenAI client."""
        client = Mock()
        mock_agent = AsyncMock()
        
        # Mock response with text attribute (like real Azure responses)
        class MockMessage:
            def __init__(self, text):
                self.text = text
        
        class MockResponse:
            def __init__(self, ticker):
                self.messages = [MockMessage(ticker)]
                self.response_id = f"resp-{ticker}"
        
        mock_agent.run.return_value = MockResponse("TSLA")
        client.create_agent.return_value = mock_agent
        return client
    
    @pytest.fixture
    def mock_yfinance_success(self):
        """Mock successful yfinance response."""
        mock_ticker = Mock()
        mock_ticker.info = {
            "regularMarketPrice": 250.45,
            "longName": "Tesla Inc",
            "currency": "USD",
            "symbol": "TSLA"
        }
        return mock_ticker
    
    @pytest.fixture
    def stock_agent(self, mock_config, mock_azure_client):
        """Create StockAgent instance for testing."""
        with patch('src.agents.stock_agent.get_config', return_value=mock_config):
            return StockAgent(config=mock_config, chat_client=mock_azure_client)
    
    @pytest.mark.parametrize("query,expected_ticker", [
        ("What's the price of Tesla?", "TSLA"),
        ("How much is Apple stock?", "AAPL"),
        ("NVIDIA price", "NVDA"),
        ("Tell me about Microsoft shares", "MSFT"),
        ("GOOGL current value", "GOOGL"),
        ("amazon stock price", "AMZN"),
    ])
    @pytest.mark.asyncio
    async def test_run_with_various_queries(self, stock_agent, mock_yfinance_success, query, expected_ticker):
        """Test the run method with various stock queries - only public API."""
        # Update mock to return the expected ticker
        class MockMessage:
            def __init__(self, text):
                self.text = text
        
        class MockResponse:
            def __init__(self, ticker):
                self.messages = [MockMessage(ticker)]
                self.response_id = f"resp-{ticker}"
        
        mock_agent = AsyncMock()
        mock_agent.run.return_value = MockResponse(expected_ticker)
        stock_agent.chat_client.create_agent.return_value = mock_agent
        
        # Mock yfinance for stock price fetching
        with patch('src.agents.stock_agent.yf.Ticker') as mock_yf_ticker:
            mock_yfinance_success.info["longName"] = f"{expected_ticker} Company"
            mock_yf_ticker.return_value = mock_yfinance_success
            
            result = await stock_agent.run(query)
            
            # Verify the agent returns a proper response
            assert result.messages is not None
            assert len(result.messages) > 0
            # The formatted response should contain the ticker and company info
            response_text = result.messages[0].text
            assert expected_ticker in response_text
            assert "$250.45" in response_text
    
    @pytest.mark.asyncio
    async def test_run_with_empty_query(self, stock_agent):
        """Test run method with empty query."""
        result = await stock_agent.run("")
        assert result.response_id == "no-query"
        assert result.messages == []
    
    @pytest.mark.asyncio
    async def test_run_with_invalid_stock_ticker(self, stock_agent):
        """Test run method when stock ticker is invalid/not found."""
        # Mock AI to return an invalid ticker
        class MockMessage:
            def __init__(self, text):
                self.text = text
        
        class MockResponse:
            def __init__(self, ticker):
                self.messages = [MockMessage(ticker)]
                self.response_id = f"resp-{ticker}"
        
        mock_agent = AsyncMock()
        mock_agent.run.return_value = MockResponse("INVALID")
        stock_agent.chat_client.create_agent.return_value = mock_agent
        
        # Mock yfinance to simulate stock not found
        with patch('src.agents.stock_agent.yf.Ticker') as mock_yf_ticker:
            mock_ticker = Mock()
            mock_ticker.info = {}  # Empty info indicates invalid ticker
            mock_ticker.history.return_value.empty = True  # No historical data
            mock_yf_ticker.return_value = mock_ticker
            
            result = await stock_agent.run("What's the price of INVALID?")
            
            # Should return an error response
            assert result.response_id == "error"
            assert len(result.messages) > 0
            assert "couldn't process" in result.messages[0].text.lower()
    
    @pytest.mark.asyncio
    async def test_run_with_ai_client_error(self, stock_agent):
        """Test run method when AI client fails."""
        # Mock AI client to raise an exception
        mock_agent = AsyncMock()
        mock_agent.run.side_effect = Exception("AI API Error")
        stock_agent.chat_client.create_agent.return_value = mock_agent
        
        result = await stock_agent.run("What's Tesla's price?")
        
        # Should return an error response
        assert result.response_id == "error"
        assert len(result.messages) > 0
        assert "couldn't process" in result.messages[0].text.lower()
    
    @pytest.mark.asyncio
    async def test_run_with_yfinance_timeout(self, stock_agent):
        """Test run method when yfinance times out."""
        # Mock AI to return valid ticker
        class MockMessage:
            def __init__(self, text):
                self.text = text
        
        class MockResponse:
            def __init__(self, ticker):
                self.messages = [MockMessage(ticker)]
                self.response_id = f"resp-{ticker}"
        
        mock_agent = AsyncMock()
        mock_agent.run.return_value = MockResponse("TSLA")
        stock_agent.chat_client.create_agent.return_value = mock_agent
        
        # Mock yfinance to timeout
        with patch('src.agents.stock_agent.yf.Ticker') as mock_yf_ticker:
            mock_yf_ticker.side_effect = TimeoutError("Request timeout")
            
            result = await stock_agent.run("What's Tesla's price?")
            
            # Should return an error response
            assert result.response_id == "error"
            assert len(result.messages) > 0
            assert "couldn't process" in result.messages[0].text.lower()
    
    @pytest.mark.asyncio
    async def test_run_successful_workflow(self, stock_agent, mock_yfinance_success):
        """Test complete successful workflow through public run method."""
        query = "What's the price of Tesla?"
        
        # Mock successful AI ticker extraction
        class MockMessage:
            def __init__(self, text):
                self.text = text
        
        class MockResponse:
            def __init__(self, ticker):
                self.messages = [MockMessage(ticker)]
                self.response_id = f"resp-{ticker}"
        
        mock_agent = AsyncMock()
        mock_agent.run.return_value = MockResponse("TSLA")
        stock_agent.chat_client.create_agent.return_value = mock_agent
        
        # Mock successful yfinance call
        with patch('src.agents.stock_agent.yf.Ticker') as mock_yf_ticker:
            mock_yf_ticker.return_value = mock_yfinance_success
            
            result = await stock_agent.run(query)
            
            # Verify successful response
            assert result.response_id == "stock-info-TSLA"
            assert len(result.messages) > 0
            
            response_text = result.messages[0].text
            assert "Tesla Inc" in response_text
            assert "TSLA" in response_text
            assert "$250.45" in response_text
            assert "USD" in response_text
    
    @pytest.mark.asyncio
    async def test_run_with_list_messages(self, stock_agent, mock_yfinance_success):
        """Test run method with list of messages instead of string."""
        messages = ["What's the price of Tesla?"]
        
        # Mock successful workflow
        class MockMessage:
            def __init__(self, text):
                self.text = text
        
        class MockResponse:
            def __init__(self, ticker):
                self.messages = [MockMessage(ticker)]
                self.response_id = f"resp-{ticker}"
        
        mock_agent = AsyncMock()
        mock_agent.run.return_value = MockResponse("TSLA")
        stock_agent.chat_client.create_agent.return_value = mock_agent
        
        with patch('src.agents.stock_agent.yf.Ticker') as mock_yf_ticker:
            mock_yf_ticker.return_value = mock_yfinance_success
            
            result = await stock_agent.run(messages)
            
            assert result.response_id == "stock-info-TSLA"
            assert "Tesla Inc" in result.messages[0].text