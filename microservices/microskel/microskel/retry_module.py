import time
from abc import ABC, abstractmethod
from microskel.log_call_module import log_call

class RetryStrategy(ABC):
    @abstractmethod
    def execute(self, func, *args, **kwargs):
        pass


class ExponentialBackoff(RetryStrategy):
    def __init__(self, initial_delay=1, max_delay=120, factor=2):
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.factor = factor

    @log_call
    def execute(self, func, *args, **kwargs):
        delay = self.initial_delay
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Exception occurred: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay = min(delay * self.factor, self.max_delay)
                if delay > self.max_delay:
                    raise e


class JitterRetry(RetryStrategy):
    def __init__(self, initial_delay=1, max_delay=60, factor=2):
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.factor = factor

    def execute(self, func, *args, **kwargs):
        delay = self.initial_delay
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if delay > self.max_delay:
                    raise e
                delay *= self.factor

RETRY_STRATEGIES = {
    'EXPONENTIAL_BACKOFF': ExponentialBackoff,
    'JITTER_RETRY': JitterRetry,
}

def get_retry_strategy(strategy_name: str):
    strategy_class = RETRY_STRATEGIES.get(strategy_name)
    if strategy_class is None:
        raise ValueError(f"Unknown retry strategy: {strategy_name}")
    return strategy_class()


def retry(strategy: RetryStrategy):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return strategy.execute(func, *args, **kwargs)
        return wrapper

    return decorator
