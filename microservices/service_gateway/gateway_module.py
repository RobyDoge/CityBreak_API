from injector import Module, Binder, singleton
from microskel.service_discovery import ServiceDiscovery
from flask import request
from decouple import config

from events_client_module import EventsClient
from weather_client_module import WeatherClient


class GatewayModule(Module):
   def __init__(self, service):
      self.service = service

   def configure(self, binder: Binder) -> None:
      events_client = EventsClient(self.service)
      binder.bind(EventsClient, to=events_client, scope=singleton)
      weather_client = WeatherClient(self.service)
      binder.bind(WeatherClient, to=weather_client, scope=singleton)


def configure_views(app):
   @app.route('/get_events/<city>')
   def get_events(city: str, events_client: EventsClient):
      app.logger.info(f'get_events/{city} called in {config("MICROSERVICE_NAME")}')
      data_from_events = events_client.get_events(city)
      my_own_data = f'Data for {city} from {config("MICROSERVICE_NAME")}'
      return f'{data_from_events} AND {my_own_data}'
   
   @app.route('/events', methods=['POST', 'PUT', 'DELETE'])
   def event_post_put_delete(events_client: EventsClient):
      from utils import proxy_request
      return proxy_request(request, f'{events_client.endpoint().to_base_url()}/events')
   

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
      
