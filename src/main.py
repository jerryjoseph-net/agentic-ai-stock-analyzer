"""Main CLI interface for the Agentic AI Stock Analyzer - Milestone 1."""
import asyncio
import logging
import sys
from typing import Optional

from utils.exceptions import StockAnalyzerError
from agents.stock_agent import StockAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StockAnalyzerCLI:
    """Command line interface for the stock analyzer - Milestone 1 simplified version."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.stock_agent: Optional[StockAgent] = None
    
    def setup(self) -> None:
        """Setup the CLI with stock agent."""
        try:
            # Initialize stock agent (simplified for Milestone 1)
            self.stock_agent = StockAgent()
            logger.info("Stock agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            print(f"❌ Setup failed: {e}")
            sys.exit(1)
    
    async def process_query(self, query: str) -> str:
        """Process a single query.
        
        Args:
            query: User's stock query
            
        Returns:
            Formatted response
        """
        try:
            response = await self.stock_agent.run(query)
            if response.messages and len(response.messages) > 0:
                return f"📈 {response.messages[0].text}"
            elif response.response_id != "error":
                return f"📈 Stock info retrieved (ID: {response.response_id})"
            else:
                return "❌ Failed to get stock information"
        except StockAnalyzerError as e:
            return f"❌ {e}"
        except Exception as e:
            logger.error(f"Unexpected error processing query: {e}")
            return f"❌ Unexpected error: {e}"
    
    async def interactive_mode(self) -> None:
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
                response = await self.process_query(query)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"❌ An error occurred: {e}")
    
    async def single_query_mode(self, query: str) -> None:
        """Process a single query and exit.
        
        Args:
            query: Stock query to process
        """
        response = await self.process_query(query)
        print(response)


async def main():
    """Main entry point."""
    cli = StockAnalyzerCLI()
    cli.setup()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        await cli.single_query_mode(query)
    else:
        # Interactive mode
        await cli.interactive_mode()


if __name__ == "__main__":
    asyncio.run(main())