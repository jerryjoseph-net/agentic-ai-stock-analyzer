"""
Stock Analysis Orchestrator using Azure AI Agent Framework

This module provides the StockAnalyzerAgent that orchestrates workflows between
multiple specialized agents for comprehensive stock analysis.
"""

import asyncio
import logging
from typing import Any
from collections.abc import Awaitable, Callable
from contextlib import AsyncExitStack

from agent_framework import AgentRunUpdateEvent, WorkflowBuilder, WorkflowOutputEvent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

try:
    from src.agents.stock_agent import stock_agent_factory
except ImportError:
    # Fallback for running from src/ directory directly
    from agents.stock_agent import stock_agent_factory  # type: ignore

logger = logging.getLogger(__name__)


class StockAnalyzerAgent:
    """
    Orchestrator agent that manages workflows by calling StockAgent through workflows.
    
    As shown in the architecture diagram:
    - Acts as orchestrator that parses intent
    - Calls StockAgent through agent-to-agent workflow calls
    - StockAgent uses its tools (yfinance API, ticker map, regex/LLM)
    """
    
    def __init__(self):
        """Initialize the StockAnalyzerAgent orchestrator."""
        self._stack = AsyncExitStack()
        self._client = None
        logger.info("StockAnalyzerAgent orchestrator initialized")
    
    async def __aenter__(self):
        credential = await self._stack.enter_async_context(AzureCliCredential())
        self._client = await self._stack.enter_async_context(
            AzureAIAgentClient(async_credential=credential)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._stack.aclose()
    
    def create_stock_workflow(self) -> Any:
        """Build WorkflowBuilder graph that runs StockAgent."""
        stock_agent = stock_agent_factory(self._client)

        workflow = (
            WorkflowBuilder()
            .add_agent(stock_agent, id="StockAgent", output_response=True)
            .set_start_executor(stock_agent)  # must be instance, not string
            .build()
        )
        return workflow
    
    async def analyze_stock(self, query: str, stream: bool = True) -> str:
        """Run orchestrated stock analysis."""
        logger.info(f"StockAnalyzerAgent orchestrating analysis for: {query}")
        workflow = self.create_stock_workflow()

        if stream:
            return await self._run_streaming_analysis(workflow, query)
        else:
            return await self._run_complete_analysis(workflow, query)
    
    def _extract_workflow_result(self, events) -> str:
        """Extract the final result from workflow events."""
        for event in events:
            if hasattr(event, 'data') and event.__class__.__name__ == 'WorkflowOutputEvent':
                return event.data
        return "No result found"
    
    async def _run_streaming_analysis(self, workflow: Any, query: str) -> str:
        """Run orchestrated analysis with simulated streaming output."""
        print(f"🔍 [StockAnalyzerAgent] Orchestrating analysis: {query}\n")

        events = await workflow.run(query)
        result = self._extract_workflow_result(events)
        
        # print("\n\n" + "=" * 60)
        # print("📊 ORCHESTRATED STOCK ANALYSIS")
        # print("=" * 60)
        # print(result)

        return result
    
    async def _run_complete_analysis(self, workflow: Any, query: str) -> str:
        """Run orchestrated analysis without streaming."""
        events = await workflow.run(query)
        return self._extract_workflow_result(events)
    


async def main() -> None:
    """Demo entry point."""
    print("=== StockAnalyzerAgent orchestrating StockAgent via Workflow ===\n")
    async with StockAnalyzerAgent() as orchestrator:
        query = "What's the price of Tesla?"
        await orchestrator.analyze_stock(query, stream=True)



if __name__ == "__main__":
    asyncio.run(main())