from microskel.service_discovery import ServiceDiscovery 
from microskel.retry_module import retry,get_class
import requests
from decouple import config


class EventsClient:
   def __init__(self, service) -> None:
      self.service = service

   @retry(get_class(config('RETRY_STRATEGY')))
   def get_events(self, city):
      endpoint = self.service.injector.get(ServiceDiscovery).discover('events')
      if not endpoint:
         return 'No endpoint', 401
      return requests.get(f'{endpoint.to_base_url()}/events/{city}').json()


   @retry(get_class(config('RETRY_STRATEGY')))
   def endpoint(self): 
      return self.service.injector.get(ServiceDiscovery).discover('events')