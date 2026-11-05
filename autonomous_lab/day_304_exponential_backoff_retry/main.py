"""
Resilient Retry Engine with Jitter
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import time
import random
from typing import Callable, Any, Tuple, Type

class RetryEngine:
    """
    Executes functions with exponential backoff and randomized jitter.
    """
    def __init__(self, max_attempts: int = 3, base_delay: float = 0.1, max_delay: float = 2.0, exceptions: Tuple[Type[Exception], ...] = (Exception,)):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exceptions = exceptions

    def calculate_delay(self, attempt: int) -> float:
        exponential = self.base_delay * (2 ** (attempt - 1))
        capped = min(self.max_delay, exponential)
        # Full jitter between 0 and capped
        return random.uniform(0, capped)

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        attempts = 0
        while True:
            attempts += 1
            try:
                return func(*args, **kwargs)
            except self.exceptions as err:
                if attempts >= self.max_attempts:
                    raise err
                delay = self.calculate_delay(attempts)
                time.sleep(delay)
