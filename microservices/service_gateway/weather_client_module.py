from microskel.service_discovery import ServiceDiscovery 
import requests


class WeatherClient:
   def __init__(self, service) -> None:
      self.service = service

   def get_weather(self, city):
      endpoint = self.service.injector.get(ServiceDiscovery).discover('weather')
      if not endpoint:
         return 'No endpoint', 401
      return requests.get(f'{endpoint.to_base_url()}/weather/{city}').json()
   
   def endpoint(self):
      return self.service.injector.get(ServiceDiscovery).discover('weather')