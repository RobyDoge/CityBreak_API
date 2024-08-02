from functools import wraps
import time
import random


class RetryStrategieModule:
      def execute(function, *args, **kwargs):
          pass


class ExponentialBackoff(RetryStrategieModule):
   def __init__(self, retry_attemps=3, factor=2, max_delay=60):
      self.retry_attemps = retry_attemps
      self.factor = factor
      self.max_delay = max_delay

   def execute(self,function, *args, **kwargs):
      for i in range(self.retry_attemps):
         try:
            return function(*args, **kwargs)
         except Exception as e:
            if i == self.retry_attemps - 1:
               raise e
            else:
               time.sleep(min(self.factor**i, self.max_delay))



class JitteredExponentialBackoff(RetryStrategieModule):
   def __init(self, jitter=0.5, retry_attemps=3, factor=2, max_delay=60):
      self.factor = factor
      self.max_delay = max_delay
      self.jitter = jitter
      self.retry_attemps = retry_attemps
   
   def execute(self,function, *args, **kwargs):
      for i in range(self.retry_attemps):
         try:
            return function(*args, **kwargs)
         except Exception as e:
            if i == self.retry_attemps - 1:
               raise e
            else:
               time.sleep(min(self.factor**i + random.random(0,self.jitter), self.max_delay))



retry_strategy_mapping = {
   'EXPONENTIAL_BACKOFF' : ExponentialBackoff,
   'JITTERED_EXPONENTIAL_BACKOFF' : JitteredExponentialBackoff
}


def get_class(retry_strategy: str):
      try:
            return retry_strategy_mapping[retry_strategy]
      except KeyError:
            raise ValueError(f'Invalid retry strategy: {retry_strategy}')


def retry(retry_strategy: RetryStrategieModule):
   def decorator(function):
      @wraps(function)
      def wrapper(*args, **kwargs):
         return retry_strategy.execute(function, *args, **kwargs)
      return wrapper
   return decorator
