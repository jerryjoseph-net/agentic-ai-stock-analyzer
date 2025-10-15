"""Main CLI interface for the Agentic AI Stock Analyzer"""

import asyncio
import logging
import sys
from dotenv import load_dotenv
from agents.stock_orchestrator import StockAnalyzerAgent

# Load environment variables from .env file
load_dotenv()

# Suppress agent_framework warnings
logging.getLogger("agent_framework._clients").setLevel(logging.ERROR)
logging.getLogger("agent_framework").setLevel(logging.ERROR)

async def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter your stock query: ").strip()
    async with StockAnalyzerAgent() as orchestrator:
        result = await orchestrator.analyze_stock(query, stream=True)
        print(result)

if __name__ == "__main__":
    asyncio.run(main())