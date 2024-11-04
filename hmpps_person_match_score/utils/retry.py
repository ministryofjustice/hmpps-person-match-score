import random
import time
from typing import Callable


class RetryExecutor:
    """
    Class to execute potentially flaky functions
    """

    MAX_RETRY_COUNT = 3
    MAX_DELAY_MS = 1000
    DELAY_BASE_MS = 50

    JITTER_MIN = 0.8
    JITTER_MAX = 1.2

    @classmethod
    def retry(
        cls,
        action: Callable,
        retry_exceptions: tuple = None,
        max_attempts: int = MAX_RETRY_COUNT,
        base_delay: int = DELAY_BASE_MS,
        max_delay: int = MAX_DELAY_MS,
    ):
        """
        Retries a function with a jittered backoff strategy.

        Args:
            func: The function to be retried.
            retry_exceptions: Exceptions that should trigger a retry (Defaults to all).
            max_attempts: Maximum number of retry attempts.
            base_delay: Base delay for exponential backoff (in seconds).
            max_delay: Maximum delay for the backoff (in seconds).

        Returns:
            The result of the function if successful.

        Raises:
            Exception: Raises the last exception if all attempts fail.
        """
        if retry_exceptions is None:
            retry_exceptions = (Exception,)

        for attempt in range(max_attempts):
            try:
                return action()
            except retry_exceptions as exception:
                # If this is the last attempt, raise the exception
                if attempt == max_attempts - 1:
                    raise exception
                # Calculate the delay with jitter
                jitter = random.uniform(cls.JITTER_MIN, cls.JITTER_MAX)  # noqa: S311
                delay = min(base_delay * pow(2, attempt), max_delay) * jitter
                time.sleep(delay / 1000)  # Convert to seconds
