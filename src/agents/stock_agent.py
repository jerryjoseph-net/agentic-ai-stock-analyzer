"""Stock Agent implementation using Azure OpenAI."""
import re
import logging
import yfinance as yf
from datetime import datetime
from typing import Dict, Any

from agent_framework.azure import AzureOpenAIChatClient
from agent_framework import BaseAgent, AgentRunResponse, ChatMessage

try:
    from src.utils.exceptions import StockNotFoundError, APIRateLimitError, AgentError
    from src.utils.config import get_config
except ImportError:
    # Fallback for running from src/ directory directly
    from utils.exceptions import StockNotFoundError, APIRateLimitError, AgentError  # type: ignore
    from utils.config import get_config  # type: ignore

logger = logging.getLogger(__name__)


class StockAgent(BaseAgent):
    """
    Agent for extracting stock tickers from user queries, fetching current stock prices, and formatting responses using Azure OpenAI and yfinance.
    Implements a single public API (`run`) for complete query-to-response workflow.
    """

    NAME = "Stock Agent"
    DESCRIPTION = "Extracts stock tickers from user queries, fetches current prices, and returns formatted responses."
    # INSTRUCTIONS is used only for the ticker extraction step via Azure OpenAI
    INSTRUCTIONS = (
        "You are a stock ticker extraction assistant. Extract the stock ticker symbol from the user's query. "
        "Return ONLY the ticker symbol (e.g., 'AAPL', 'TSLA', 'MSFT'). If multiple tickers are mentioned, return the first one. "
        "If no valid ticker is found, return 'UNKNOWN'. Do not include any explanation or additional text. Ticker symbols should be uppercase."
    )

    def __init__(
            self, 
            config=None, 
            chat_client=None, 
            **kwargs):
        config = config if config else get_config()
        chat_client = chat_client if chat_client else AzureOpenAIChatClient(
            endpoint=config.azure_ai_endpoint,
            deployment_name=config.azure_ai_model_deployment,
            api_version=config.azure_ai_api_version,
            api_key=config.azure_ai_api_key
        )
        super().__init__(
            name=self.NAME, 
            description=self.DESCRIPTION, 
            **kwargs)
        self.config = config
        self.chat_client = chat_client

        logger.info("StockAgent initialized with AzureOpenAIChatClient and BaseAgent")

    # ---------------------------------------------------------
    # Core execution - PUBLIC API
    # ---------------------------------------------------------
    async def run(self, messages=None, *, thread=None, **kwargs):
        """
        Run the agent to extract ticker and fetch stock information.
        This is the main public interface for the StockAgent.
        
        Args:
            messages: String query or list of messages
            thread: Thread context (unused)
            **kwargs: Additional arguments
            
        Returns:
            AgentRunResponse with stock information
        """
        query = messages if isinstance(messages, str) else (messages[0] if messages else "")
        query = query.strip()

        if not query:
            return AgentRunResponse(messages=[], response_id="no-query")
        
        try:
            # Extract ticker from query
            ticker = await self._extract_ticker(query)
            
            # Fetch stock price information
            stock_data = self._fetch_stock_price(ticker)
            
            # Format response
            formatted_response = self._format_response(stock_data)
            
            return AgentRunResponse(
                messages=[ChatMessage(role="assistant", text=formatted_response)], 
                response_id=f"stock-info-{ticker}"
            )
            
        except Exception as e:
            logger.error(f"Agent run failed for query '{query}': {e}")
            return AgentRunResponse(
                messages=[ChatMessage(role="assistant", text=f"Sorry, I couldn't process your request: {e}")], 
                response_id="error"
            )
    
    # ---------------------------------------------------------
    # Internal helpers - PRIVATE METHODS
    # ---------------------------------------------------------
    async def _extract_ticker(self, query: str) -> str:
        """Extract stock ticker from natural language query using Agent Framework agent.
        
        Args:
            query: User's natural language query
            
        Returns:
            Stock ticker symbol (e.g., 'TSLA')
            
        Raises:
            AgentError: If ticker extraction fails
        """
        try:
            if not query or not query.strip():
                raise AgentError("Query cannot be empty")
            
            agent = self.chat_client.create_agent(
                instructions=self.INSTRUCTIONS,
                name=self.NAME
            )
            response = await agent.run(query)
            
            # AgentRunResponse: ticker is in response.messages[0].text if present
            if hasattr(response, "messages") and response.messages:
                msg = response.messages[0]
                # Try different attributes to get the content
                if hasattr(msg, "text") and msg.text:
                    ticker = str(msg.text).strip().upper()
                elif hasattr(msg, "contents") and msg.contents:
                    ticker = str(msg.contents).strip().upper()
                elif hasattr(msg, "content"):
                    ticker = str(msg.content).strip().upper()
                else:
                    ticker = str(msg).strip().upper()
            elif hasattr(response, "response_id"):
                ticker = str(response.response_id).strip().upper()
            else:
                ticker = "UNKNOWN"
            # Validate ticker format
            if ticker == "UNKNOWN" or not self._validate_ticker(ticker):
                raise AgentError(f"Could not extract valid ticker from query: {query}")
            logger.info(f"Extracted ticker '{ticker}' from query: {query}")
            return ticker
            
        except Exception as e:
            logger.error(f"Failed to extract ticker from query '{query}': {e}")
            raise AgentError(f"Ticker extraction failed: {e}")
    
    def _validate_ticker(self, ticker: str) -> bool:
        """Validate ticker symbol format.
        
        Args:
            ticker: Stock ticker to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not ticker or ticker == "UNKNOWN":
            return False
        
        # Basic validation: 1-5 uppercase letters
        pattern = r'^[A-Z]{1,5}$'
        return bool(re.match(pattern, ticker))
    
    def _fetch_stock_price(self, ticker: str) -> Dict[str, Any]:
        """Fetch current stock price for given ticker.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with stock information
            
        Raises:
            StockNotFoundError: If ticker is invalid or not found
            APIRateLimitError: If API requests fail
        """
        try:
            logger.info(f"Fetching stock price for {ticker}")
            
            # Validate ticker format
            if not self._validate_ticker(ticker):
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
    
    def _format_response(self, stock_data: Dict[str, Any]) -> str:
        """Format stock data into human-readable response.
        
        Args:
            stock_data: Stock information dictionary
            
        Returns:
            Formatted response string
        """
        return (f"{stock_data['company_name']} ({stock_data['ticker']}): "
                f"${stock_data['price']:.2f} {stock_data['currency']} "
                f"({stock_data['change']})")
