import logging
import sys

def setup_logger():
    """
    Configures and returns a structured logger for the application.
    """
    logger = logging.getLogger("traffic_violation_app")
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Standard format containing timestamp, severity level, module, and log content
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logger()
