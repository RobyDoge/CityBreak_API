from microskel.service_discovery import ServiceDiscovery
import requests
from decouple import config
from microskel.retry_module import retry
from microskel.retry_module import get_retry_strategy
from microskel.log_call_module import log_call
class EventsClient:
    def __init__(self, service) -> None:
        self.service = service
    def get_events(self, city):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('events')
        if not endpoint:
            return 'No endpoint', 401
        return requests.get(f'{endpoint.to_base_url()}/events/{city}').json()

    @log_call
    @retry(get_retry_strategy(config('RETRY_STRATEGY')))
    def get_endpoint(self):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('events')
        if not endpoint:
            raise Exception('Failed to discover service_events endpoint')
        return endpoint
