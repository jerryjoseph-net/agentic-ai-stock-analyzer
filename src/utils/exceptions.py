"""Custom exceptions for the stock analyzer."""


class StockAnalyzerError(Exception):
    """Base exception for stock analyzer."""
    pass


class StockNotFoundError(StockAnalyzerError):
    """Raised when a stock ticker is not found or invalid."""
    pass


class APIRateLimitError(StockAnalyzerError):
    """Raised when API rate limits are exceeded."""
    pass


class ConfigurationError(StockAnalyzerError):
    """Raised when configuration is invalid."""
    pass


class AgentError(StockAnalyzerError):
    """Raised when agent processing fails."""
    pass