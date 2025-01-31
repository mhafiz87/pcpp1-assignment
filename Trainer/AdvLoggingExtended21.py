import logging
import logging.handlers
import time
import traceback
from threading import Thread, current_thread

# Custom log level
TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, "TRACE")

def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, message, args, **kwargs)

logging.Logger.trace = trace

# Logger configuration
logger = logging.getLogger("AdvancedLogger")
logger.setLevel(logging.DEBUG)

# File handler with log rotation
file_handler = logging.handlers.RotatingFileHandler(
    "advanced_troubleshooting.log", maxBytes=5000, backupCount=3
)
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter to include contextual information
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - [%(threadName)s] - %(funcName)s:%(lineno)d - %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Adding handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Example function to demonstrate exception handling
def simulate_error():
    try:
        1 / 0  # Intentional error
    except Exception as e:
        logger.error("An error occurred: %s", e)
        logger.debug("Exception details:", exc_info=True)

# Example function to demonstrate performance logging
def long_running_task():
    start_time = time.time()
    logger.info("Starting a long-running task.")
    time.sleep(2)  # Simulate task
    end_time = time.time()
    logger.info("Task completed in %.2f seconds.", end_time - start_time)

# Threaded example to demonstrate thread-specific logging
def threaded_function():
    logger.debug("Thread started.")
    time.sleep(1)
    logger.debug("Thread finished.")

# Main function demonstrating all techniques
def main():
    logger.info("Application started.")

    # Custom log level example
    logger.trace("This is a trace-level log for detailed tracing.")

    # Simulate an error
    simulate_error()

    # Performance logging
    long_running_task()

    # Multithreaded example
    threads = []
    for i in range(3):
        thread = Thread(target=threaded_function, name=f"Worker-{i}")
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    logger.info("Application ended.")

if __name__ == "__main__":
    main()
