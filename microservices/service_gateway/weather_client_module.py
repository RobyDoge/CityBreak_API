from injector import Module, Binder, singleton
from flask import request

from microskel.service_discovery import ServiceDiscovery 
import requests
from decouple import config


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

class GatewayModule(Module):
   def __init__(self, service):
      self.service = service

   def configure(self, binder: Binder) -> None:
      weather_client = WeatherClient(self.service)
      binder.bind(WeatherClient, to=weather_client, scope=singleton)


def configure_views(app):
   @app.route('/get_weather/<city>')
   def get_weather(city: str, weather_client: WeatherClient):
      app.logger.info(f'get_weather/{city} called in {config("MICROSERVICE_NAME")}')
      data_from_weather = weather_client.get_weather(city)
      my_own_data = f'Data for {city} from {config("MICROSERVICE_NAME")}'
      return f'{data_from_weather} AND {my_own_data}'
   
   @app.route('/weather', methods=['POST', 'PUT', 'DELETE'])
   def weather_post_put_delete(weather_client: WeatherClient):
      from utils import proxy_request
      return proxy_request(request, f'{weather_client.endpoint().to_base_url()}/weather')
      

