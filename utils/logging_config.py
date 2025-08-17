import logging
import sys


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Configure logging with consistent formatting across the entire module.
    
    Args:
        level: Logging level (default: logging.INFO)
    """
    # Create a custom formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configure the root logger
    root_logger = logging.getLogger()
    
    # Clear any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create and configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    
    # Add handler to root logger
    root_logger.addHandler(console_handler)
    root_logger.setLevel(level)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Logger name (typically __name__ from calling module)
    
    Returns:
        Logger instance with consistent formatting
    """
    return logging.getLogger(name)
