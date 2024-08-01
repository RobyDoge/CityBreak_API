from microskel.service_discovery import ServiceDiscovery 
import requests


class EventsClient:
   def __init__(self, service) -> None:
      self.service = service

   def get_events(self, city):
      endpoint = self.service.injector.get(ServiceDiscovery).discover('events')
      if not endpoint:
         return 'No endpoint', 401
      return requests.get(f'{endpoint.to_base_url()}/events/{city}').json()
   
   def endpoint(self): 
      return self.service.injector.get(ServiceDiscovery).discover('events')