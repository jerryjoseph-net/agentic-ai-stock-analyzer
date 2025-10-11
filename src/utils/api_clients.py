"""Azure AI client setup and configuration."""
import logging
from typing import Optional
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

from .config import AgentConfig
from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)


def create_azure_ai_client(config: Optional[AgentConfig] = None) -> ChatCompletionsClient:
    """Create and configure Azure AI client.
    
    Args:
        config: Optional configuration, will load from env if not provided
        
    Returns:
        Configured Azure AI client
        
    Raises:
        ConfigurationError: If configuration is invalid
    """
    try:
        if not config:
            from .config import get_config
            config = get_config()
        
        client = ChatCompletionsClient(
            endpoint=config.azure_ai_endpoint,
            credential=AzureKeyCredential(config.azure_ai_api_key)
        )
        
        logger.info(f"Azure AI client created for endpoint: {config.azure_ai_endpoint}")
        return client
        
    except Exception as e:
        logger.error(f"Failed to create Azure AI client: {e}")
        raise ConfigurationError(f"Azure AI client creation failed: {e}")