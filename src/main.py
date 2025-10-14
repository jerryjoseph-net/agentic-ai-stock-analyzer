"""Main CLI interface for the Agentic AI Stock Analyzer"""

import logging
import sys

try:
    from src.utils.exceptions import StockAnalyzerError
    from src.agents.stock_agent import extract_ticker, fetch_stock_price, format_stock_response
except ImportError:
    # Fallback for running from src/ directory directly
    from utils.exceptions import StockAnalyzerError  # type: ignore
    from agents.stock_agent import extract_ticker, fetch_stock_price, format_stock_response  # type: ignore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StockAnalyzerCLI:
    """Command line interface for the stock analyzer"""
    
    def __init__(self):
        """Initialize the CLI."""
        logger.info("StockAnalyzer CLI initialized")
    
    def setup(self) -> None:
        """Setup the CLI (no setup needed for function-based approach)."""
        logger.info("Setup complete - using function-based stock tools")
    
    def process_query(self, query: str) -> str:
        """Process a single query using function-based tools.
        
        Args:
            query: User's stock query
            
        Returns:
            Formatted response
        """
        try:
            # Extract ticker from query
            ticker = extract_ticker(query)
            
            if ticker == "UNKNOWN":
                return "❌ Sorry, I couldn't identify a stock ticker in your query."
            
            # Fetch stock price information
            stock_data = fetch_stock_price(ticker)
            
            # Format response
            formatted_response = format_stock_response(stock_data)
            
            return f"📈 {formatted_response}"
            
        except StockAnalyzerError as e:
            return f"❌ {e}"
        except Exception as e:
            logger.error(f"Unexpected error processing query: {e}")
            return f"❌ Unexpected error: {e}"
    
    def interactive_mode(self) -> None:
        """Run the CLI in interactive mode."""
        print("🚀 Agentic AI Stock Analyzer - Milestone 1")
        print("=" * 50)
        print("Ask me about stock prices! (Type 'quit' to exit)")
        print("Examples:")
        print("  - What's the price of Tesla?")
        print("  - How much is Apple stock?")
        print("  - NVIDIA current price")
        print()
        
        while True:
            try:
                query = input("📊 Your query: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not query:
                    print("Please enter a query.")
                    continue
                
                print("🤖 Processing...")
                response = self.process_query(query)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"❌ An error occurred: {e}")
    
    def single_query_mode(self, query: str) -> None:
        """Process a single query and exit.
        
        Args:
            query: Stock query to process
        """
        response = self.process_query(query)
        print(response)


def main():
    """Main entry point."""
    cli = StockAnalyzerCLI()
    cli.setup()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        cli.single_query_mode(query)
    else:
        # Interactive mode
        cli.interactive_mode()


if __name__ == "__main__":
    main()