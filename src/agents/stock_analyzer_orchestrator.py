"""
Stock Analysis Orchestrator using Azure AI Agent Framework

This module provides the StockAnalyzerOrchestrator - a proper AI agent that coordinates
and delegates to specialized agents (StockAgent, etc.) as tools for comprehensive
stock analysis and multi-agent workflows.
"""

import asyncio
import logging
from typing import Any, Annotated
from contextlib import AsyncExitStack

from agent_framework import WorkflowBuilder
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from pydantic import Field

try:
    from src.agents.stock_agent import stock_agent_factory
except ImportError:
    # Fallback for running from src/ directory directly
    from agents.stock_agent import stock_agent_factory  # type: ignore

logger = logging.getLogger(__name__)


def create_stock_analyzer_orchestrator(client: AzureAIAgentClient) -> Any:
    """Factory function to create StockAnalyzerOrchestrator as an AI agent with other agents as tools."""

    async def delegate_to_stock_agent(
        query: Annotated[str, Field(description="The stock query to delegate to StockAgent")]
    ) -> str:
        """Delegate stock analysis query to StockAgent through workflow."""
        logger.info(f"StockAnalyzerOrchestrator delegating query to StockAgent: {query}")

        stock_agent = stock_agent_factory(client)
        workflow = (
            WorkflowBuilder()
            .add_agent(stock_agent, id="StockAgent", output_response=True)
            .set_start_executor(stock_agent)
            .build()
        )

        events = await workflow.run(query)

        # Extract result from workflow events
        for event in events:
            if hasattr(event, 'data') and event.__class__.__name__ == 'WorkflowOutputEvent':
                return str(event.data) if event.data is not None else "No result found"

        return "No result found"

    # Create the StockAnalyzerOrchestrator as a proper AI agent with other agents as tools
    agent = client.create_agent(
        name="StockAnalyzerOrchestrator",
        instructions="""You are the main stock analysis orchestrator agent. Your role is to:
1. Understand user queries about stock prices, financial information, and analysis requests
2. Coordinate and delegate to specialized agents using your available tools:
   - StockAgent: For fetching current stock prices and basic stock information
   - (Future: CurrencyAgent, ReportAgent, etc.)
3. Synthesize results from multiple agents when needed
4. Provide comprehensive, well-formatted responses to users

When users ask about stock information, use the delegate_to_stock_agent tool to get the data.
You are the main coordinator that orchestrates the multi-agent workflow.""",
        tools=[delegate_to_stock_agent],
    )

    return agent


class StockAnalyzerOrchestrator:
    """
    Main orchestrator AI agent that coordinates multi-agent workflows for stock analysis.

    This is a proper AI agent (not just a management class) that:
    - Has other specialized agents (StockAgent, etc.) configured as tools
    - Reasons about user queries and delegates to appropriate agents
    - Coordinates multi-agent workflows and synthesizes results
    - Manages Azure AI client lifecycle for the agent ecosystem
    """

    def __init__(self) -> None:
        """Initialize the orchestrator agent."""
        self._stack = AsyncExitStack()
        self._client: Any = None
        self._orchestrator_agent: Any = None
        logger.info("StockAnalyzerOrchestrator (AI agent) initialized")

    async def __aenter__(self) -> "StockAnalyzerOrchestrator":
        credential = await self._stack.enter_async_context(AzureCliCredential())
        self._client = await self._stack.enter_async_context(
            AzureAIAgentClient(async_credential=credential)
        )
        self._orchestrator_agent = create_stock_analyzer_orchestrator(self._client)
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self._stack.aclose()

    async def analyze_stock(self, query: str) -> str:
        """Run stock analysis through the orchestrator AI agent."""
        logger.info(f"StockAnalyzerOrchestrator (AI agent) analyzing: {query}")

        if not self._orchestrator_agent:
            raise RuntimeError("Orchestrator agent not initialized. Use 'async with' context manager.")

        # Run the orchestrator agent with the query - it will delegate to other agents as needed
        result = await self._orchestrator_agent.run(query)
        # Extract text from AgentRunResponse
        return result.text if hasattr(result, 'text') else str(result)
    


async def main() -> None:
    """Demo entry point."""
    print("=== StockAnalyzerOrchestrator (AI Agent) coordinating StockAgent via delegation ===\n")
    async with StockAnalyzerOrchestrator() as orchestrator:
        query = "What's the price of Tesla?"
        result = await orchestrator.analyze_stock(query)
        print(result)



if __name__ == "__main__":
    asyncio.run(main())