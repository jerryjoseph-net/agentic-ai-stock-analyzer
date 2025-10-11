"""Pytest configuration and fixtures."""
import pytest
from unittest.mock import Mock, patch
import os
import sys

# Add src to Python path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def mock_azure_openai_client():
    """Mock Azure OpenAI client for testing."""
    mock_client = Mock()
    
    # Mock chat completions response
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message = Mock()
    mock_response.choices[0].message.content = "TSLA"
    
    mock_client.chat.completions.create.return_value = mock_response
    return mock_client

@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    mock_config = Mock()
    mock_config.azure_ai_endpoint = "https://test-endpoint.openai.azure.com/"
    mock_config.azure_ai_api_key = "test-api-key"
    mock_config.azure_ai_api_version = "2024-12-01-preview"
    mock_config.azure_ai_model_deployment = "o3-mini"
    return mock_config

@pytest.fixture
def sample_stock_data():
    """Sample stock data for testing."""
    return {
        "ticker": "TSLA",
        "company_name": "Tesla Inc",
        "price": 250.45,
        "currency": "USD",
        "timestamp": "2025-10-10T10:30:00Z",
        "change": "+2.15%"
    }

@pytest.fixture
def mock_yfinance_ticker():
    """Mock yfinance ticker for testing."""
    mock_ticker = Mock()
    mock_ticker.info = {
        "regularMarketPrice": 250.45,
        "longName": "Tesla Inc",
        "symbol": "TSLA",
        "currency": "USD"
    }
    
    # Mock history data properly
    mock_hist = Mock()
    mock_hist.empty = False
    mock_close = Mock()
    mock_close.iloc = Mock()
    mock_close.iloc.__getitem__ = Mock(return_value=250.45)
    mock_hist.__getitem__ = Mock(return_value=mock_close)
    mock_ticker.history.return_value = mock_hist
    
    return mock_ticker