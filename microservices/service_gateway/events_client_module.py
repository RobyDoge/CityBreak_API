from injector import Module, Binder, singleton
from flask import request

from microskel.service_discovery import ServiceDiscovery 
import requests
from decouple import config


class EventsClient:
   def __init__(self, service) -> None:
      self.service = service

   def get_events(self, city):
      endpoint = self.service.injector.get(ServiceDiscovery).discover('events')
      if not endpoint:
         return 'No endpoint', 401
      return requests.get(f'{endpoint.to_base_url()}/events/{city}').json()
   

class GatewayModule(Module):
   def __init__(self, service):
      self.service = service

   def configure(self, binder: Binder) -> None:
      events_client = EventsClient(self.service)
      binder.bind(EventsClient, to=events_client, scope=singleton)


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