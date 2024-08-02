from microskel.service_discovery import ServiceDiscovery 
from microskel.retry_module import retry,get_class
import requests
from decouple import config


class WeatherClient:
   def __init__(self, service) -> None:
      self.service = service

   @retry(get_class(config('RETRY_STRATEGY')))
   def get_weather(self, city):
      endpoint = self.service.injector.get(ServiceDiscovery).discover('weather')
      if not endpoint:
         return 'No endpoint', 401
      return requests.get(f'{endpoint.to_base_url()}/weather/{city}').json()
   

   @retry(get_class(config('RETRY_STRATEGY')))
   def endpoint(self):
      return self.service.injector.get(ServiceDiscovery).discover('weather')