"""
Stock Agent implementation using Azure AI Agent Framework

This module provides function-based tools for stock price analysis including
ticker extraction, price fetching, and response formatting.
"""

import asyncio
import re
import logging
import yfinance as yf
from datetime import datetime
from typing import Dict, Any, Annotated

from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential

from pydantic import Field

try:
    from src.utils.exceptions import StockNotFoundError, APIRateLimitError
except ImportError:
    # Fallback for running from src/ directory directly
    from utils.exceptions import StockNotFoundError, APIRateLimitError  # type: ignore

logger = logging.getLogger(__name__)


def extract_ticker(
    query: Annotated[str, Field(description="The user query to extract stock ticker from.")]
) -> str:
    """Extract stock ticker from natural language query using regex patterns."""
    if not query or not query.strip():
        return "UNKNOWN"
    
    # Company name to ticker mapping
    ticker_map = {
        'tesla': 'TSLA',
        'apple': 'AAPL',
        'microsoft': 'MSFT',
        'amazon': 'AMZN',
        'google': 'GOOGL',
        'meta': 'META',
        'nvidia': 'NVDA'
    }
    
    # Check for company names first
    query_lower = query.lower()
    for company, ticker in ticker_map.items():
        if company in query_lower:
            return ticker
    
    # Look for direct ticker symbols
    ticker_match = re.search(r'\b([A-Z]{1,5})\b', query)
    if ticker_match:
        ticker = ticker_match.group(1)
        if validate_ticker(ticker):
            return ticker
    
    return "UNKNOWN"


def validate_ticker(ticker: str) -> bool:
    """Validate ticker symbol format."""
    if not ticker or ticker == "UNKNOWN":
        return False
    
    # Basic validation: 1-5 uppercase letters
    pattern = r'^[A-Z]{1,5}$'
    return bool(re.match(pattern, ticker))


def fetch_stock_price(
    ticker: Annotated[str, Field(description="The stock ticker symbol to fetch price for.")]
) -> Dict[str, Any]:
    """Fetch current stock price for given ticker using yfinance."""
    try:
        logger.info(f"Fetching stock price for {ticker}")
        
        # Validate ticker format
        if not validate_ticker(ticker):
            raise StockNotFoundError(f"Invalid ticker format: {ticker}")
        
        # Get stock data from yfinance
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Check if ticker exists
        if not info or 'regularMarketPrice' not in info:
            # Try alternative method
            hist = stock.history(period="1d")
            if hist.empty:
                raise StockNotFoundError(f"Stock not found: {ticker}")
            current_price = float(hist['Close'].iloc[-1])
            company_name = info.get('longName', ticker)
        else:
            current_price = float(info['regularMarketPrice'])
            company_name = info.get('longName', ticker)
        
        # Calculate change (simplified for now)
        change = "+0.00%"  # TODO: Implement proper change calculation
        
        result = {
            "ticker": ticker,
            "company_name": company_name,
            "price": current_price,
            "currency": info.get('currency', 'USD'),
            "timestamp": datetime.now().isoformat(),
            "change": change
        }
        
        logger.info(f"Successfully fetched {ticker}: ${current_price}")
        return result
        
    except TimeoutError as e:
        logger.error(f"Timeout fetching {ticker}: {e}")
        raise APIRateLimitError(f"Request timeout for {ticker}")
    except StockNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch {ticker}: {e}")
        raise StockNotFoundError(f"Failed to fetch stock data for {ticker}: {e}")


def format_stock_response(
    stock_data: Annotated[Dict[str, Any], Field(description="Stock data dictionary to format.")]
) -> str:
    """Format stock data into human-readable response."""
    return (f"{stock_data['company_name']} ({stock_data['ticker']}): "
            f"${stock_data['price']:.2f} {stock_data['currency']} "
            f"({stock_data['change']})")


def stock_agent_factory(client=None):
    """Factory for StockAgent instance for orchestration workflows."""
    if client is None:
        client = AzureAIAgentClient(async_credential=AzureCliCredential())
    agent = client.create_agent(
        name="StockAgent",
        instructions="You are a helpful stock analysis agent. Use the provided tools to extract tickers, fetch prices, and format responses.",
        tools=[extract_ticker, fetch_stock_price, format_stock_response],
    )
    return agent


async def main() -> None:
    """Main entry point for stock agent example."""
    print("=== Stock Agent with Function-based Tools ===\n")
    
    # Run stock agent
    await stock_agent_factory()


if __name__ == "__main__":
    asyncio.run(main())
