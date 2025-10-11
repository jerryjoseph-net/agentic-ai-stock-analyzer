"""Configuration management for the stock analyzer."""
import os
from typing import Optional
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables
load_dotenv()

@dataclass
class AgentConfig:
    """Configuration for the stock agent."""
    azure_ai_endpoint: str
    azure_ai_api_key: str
    azure_ai_api_version: str = "2024-12-01-preview"
    azure_ai_model_deployment: str = "o3-mini"
    rate_limit: int = 100
    timeout: int = 30
    log_level: str = "INFO"
    debug: bool = False

    @classmethod
    def from_env(cls) -> "AgentConfig":
        """Create configuration from environment variables."""
        return cls(
            azure_ai_endpoint=os.getenv("AZURE_AI_ENDPOINT", ""),
            azure_ai_api_key=os.getenv("AZURE_AI_API_KEY", ""),
            azure_ai_api_version=os.getenv("AZURE_AI_API_VERSION", "2024-12-01-preview"),
            azure_ai_model_deployment=os.getenv("AZURE_AI_MODEL_DEPLOYMENT", "o3-mini"),
            rate_limit=int(os.getenv("RATE_LIMIT", "100")),
            timeout=int(os.getenv("TIMEOUT", "30")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            debug=os.getenv("DEBUG", "False").lower() == "true"
        )

    def validate(self) -> None:
        """Validate required configuration values."""
        if not self.azure_ai_endpoint:
            raise ValueError("AZURE_AI_ENDPOINT is required")
        if not self.azure_ai_api_key:
            raise ValueError("AZURE_AI_API_KEY is required")


def get_config() -> AgentConfig:
    """Get validated configuration."""
    config = AgentConfig.from_env()
    config.validate()
    return config