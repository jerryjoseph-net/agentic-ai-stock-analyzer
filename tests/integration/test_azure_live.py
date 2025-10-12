"""
Live Azure integration test (no mocking).
This test will make a real call to Azure OpenAI using credentials from .env.
Run only when you want to verify real connectivity and API response.
"""
import pytest
import asyncio
from src.agents.stock_agent import StockAgent
from src.utils.exceptions import AgentError

@pytest.mark.live
def test_real_azure_ticker_extraction():
    """Test real Azure OpenAI integration - only runs with explicit environment setup."""
    agent = StockAgent()
    query = "What's the price of Tesla?"
    try:
        result = asyncio.run(agent.run(query))
        assert result.response_id.startswith("stock-info")  # Accept any valid response
        assert len(result.messages) > 0
        print(f"Azure returned result: {result.messages[0].text}")
    except AgentError as e:
        pytest.fail(f"Azure call failed: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")
