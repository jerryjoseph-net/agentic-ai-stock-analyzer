# """
# End-to-end tests for deployed agent in Azure AI Foundry.
# These tests verify the agent works correctly in the cloud environment.
# """

# import os
# import sys
# import pytest
# from azure.identity import DefaultAzureCredential
# from azure.keyvault.secrets import SecretClient

# # Add src to path for imports
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# from agents.stock_agent import StockAgent


# import pytest

# @pytest.mark.live
# class TestDeployedAgent:
#     """Test suite for the deployed stock agent in Azure."""
    
#     @pytest.fixture(scope="class")
#     def deployed_agent(self):
#         """Create a stock agent configured for the deployed Azure environment."""
#         # Get Key Vault configuration from environment
#         key_vault_uri = os.getenv('KEY_VAULT_URI')
#         if not key_vault_uri:
#             pytest.skip("KEY_VAULT_URI not configured - skipping deployed agent tests")
        
#         # Initialize Azure credentials
#         credential = DefaultAzureCredential()
#         secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)
        
#         # Get secrets from Key Vault
#         try:
#             api_key_secret = secret_client.get_secret("AZURE-AI-API-KEY")
#             endpoint_secret = secret_client.get_secret("AZURE-AI-ENDPOINT")
            
#             api_key = api_key_secret.value
#             endpoint = endpoint_secret.value
            
#         except Exception as e:
#             pytest.skip(f"Failed to retrieve secrets from Key Vault: {e}")
        
#         # Create agent with Azure configuration
#         agent = StockAgent(
#             api_key=api_key,
#             endpoint=endpoint,
#             deployment_name="gpt-4.1-nano",
#             api_version="2024-12-01-preview"
#         )
        
#         return agent
    
#     @pytest.mark.live
#     def test_agent_initialization(self, deployed_agent):
#         """Test that the deployed agent initializes correctly."""
#         assert deployed_agent is not None
#         assert deployed_agent.client is not None
    
#     @pytest.mark.live
#     def test_ticker_extraction_basic(self, deployed_agent):
#         """Test basic ticker extraction functionality in the deployed environment."""
#         test_query = "What's the current price of Apple stock?"
        
#         result = deployed_agent.extract_ticker(test_query)
        
#         assert result is not None
#         assert "AAPL" in result.upper()
    
#     @pytest.mark.live
#     def test_ticker_extraction_multiple(self, deployed_agent):
#         """Test extraction of multiple tickers in the deployed environment."""
#         test_query = "Compare Microsoft and Google stocks"
        
#         result = deployed_agent.extract_ticker(test_query)
        
#         assert result is not None
#         # Should contain both MSFT and GOOGL
#         result_upper = result.upper()
#         assert "MSFT" in result_upper or "MICROSOFT" in result_upper
#         assert "GOOGL" in result_upper or "GOOGLE" in result_upper or "GOOG" in result_upper
    
#     def test_error_handling(self, deployed_agent):
#         """Test error handling in the deployed environment."""
#         # Test with empty query
#         result = deployed_agent.extract_ticker("")
#         assert result is not None  # Should handle gracefully
        
#         # Test with non-stock related query
#         result = deployed_agent.extract_ticker("What's the weather like?")
#         assert result is not None  # Should handle gracefully
    
#     def test_response_format(self, deployed_agent):
#         """Test that responses are properly formatted."""
#         test_query = "Tell me about Tesla stock performance"
        
#         result = deployed_agent.extract_ticker(test_query)
        
#         assert result is not None
#         assert isinstance(result, str)
#         assert len(result.strip()) > 0
    
#     @pytest.mark.slow
#     def test_concurrent_requests(self, deployed_agent):
#         """Test handling of concurrent requests to the deployed agent."""
#         import concurrent.futures
        
#         queries = [
#             "What's Apple's stock price?",
#             "How is Microsoft performing?",
#             "Tell me about Tesla",
#             "Amazon stock analysis",
#             "Google vs Meta comparison"
#         ]
        
#         with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#             futures = [
#                 executor.submit(deployed_agent.extract_ticker, query)
#                 for query in queries
#             ]
            
#             results = []
#             for future in concurrent.futures.as_completed(futures, timeout=30):
#                 result = future.result()
#                 assert result is not None
#                 results.append(result)
        
#         assert len(results) == len(queries)
    
#     def test_performance_baseline(self, deployed_agent):
#         """Test that the deployed agent meets performance baselines."""
#         import time
        
#         test_query = "What's the current price of Apple stock?"
        
#         start_time = time.time()
#         result = deployed_agent.extract_ticker(test_query)
#         end_time = time.time()
        
#         response_time = end_time - start_time
        
#         assert result is not None
#         # Response should be under 10 seconds for a simple query
#         assert response_time < 10.0, f"Response time {response_time:.2f}s exceeds 10s threshold"


# if __name__ == "__main__":
#     # Run tests when executed directly
#     pytest.main([__file__, "-v", "--tb=short"])