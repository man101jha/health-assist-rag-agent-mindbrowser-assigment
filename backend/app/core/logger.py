import logging
import sys

def setup_logger():
    logger=logging.getLogger("health_assistant")
    logger.setLevel(logging.INFO)
    formatter=logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    
    # Console Handler (Standard Output)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    # Avoid duplicate logs if handler already exists
    if not logger.handlers:
        logger.addHandler(handler)
    return logger
logger = setup_logger()