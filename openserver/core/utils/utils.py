import logging
import time

# Create a logger object
logger: logging.Logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('logs.log')
console_handler = logging.StreamHandler()

# Set the logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def trim_string(string, count: int) -> str:
    words = string.split()
    trimmed_words = words[:count]
    trimmed_string = ' '.join(trimmed_words)
    return trimmed_string

def run_with_time(func):
    start_time = time.time()

    func()

    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(execution_time)
