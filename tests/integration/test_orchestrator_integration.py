"""Integration tests for StockAnalyzerOrchestrator."""

import pytest
from src.agents.stock_analyzer_orchestrator import StockAnalyzerOrchestrator


class TestStockAnalyzerOrchestratorIntegration:
    """Integration tests for the StockAnalyzerOrchestrator."""
    
    @pytest.mark.live
    @pytest.mark.asyncio
    async def test_orchestrator_delegates_to_stock_agent(self):
        """Test that orchestrator properly delegates to StockAgent and returns real stock data."""
        async with StockAnalyzerOrchestrator() as orchestrator:
            result = await orchestrator.analyze_stock("What's the price of Tesla?")
            
            # Should get actual stock data
            assert "TSLA" in result or "Tesla" in result, "Result should contain actual Tesla stock information"
            assert "$" in result, "Result should contain price information with $ symbol"
            assert len(result) > 20, "Should return meaningful stock response"
    
    @pytest.mark.live
    @pytest.mark.asyncio
    async def test_orchestrator_returns_valid_stock_format(self):
        """Test that orchestrator returns properly formatted stock information."""
        async with StockAnalyzerOrchestrator() as orchestrator:
            result = await orchestrator.analyze_stock("Apple stock price")
            
            # Should get properly formatted stock response
            assert isinstance(result, str), "Result should be a string"
            assert len(result) > 20, "Result should be a meaningful response"
            assert "AAPL" in result or "Apple" in result, "Should contain Apple stock information"