"""Main CLI interface for the Agentic AI Stock Analyzer"""

import asyncio
import logging
import sys
from dotenv import load_dotenv
from agents.stock_analyzer_orchestrator import StockAnalyzerOrchestrator

# Load environment variables from .env file
load_dotenv()

# Suppress agent_framework warnings
logging.getLogger("agent_framework._clients").setLevel(logging.ERROR)
logging.getLogger("agent_framework").setLevel(logging.ERROR)

async def main() -> None:
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter your stock query: ").strip()
    async with StockAnalyzerOrchestrator() as orchestrator:
        result = await orchestrator.analyze_stock(query)
        print(result)

if __name__ == "__main__":
    asyncio.run(main())