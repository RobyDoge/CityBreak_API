from decouple import config
import random
import requests
import time


class LoadBalancer():
   def __init__(self, loadbalancer):
      self.loadbalancer = loadbalancer

   def get_registration(self, registrations):
      match self.loadbalancer:
         case 'random':
            return self.get_random(registrations)
         case 'round-robin':
            return self.get_round_robin(registrations)
         case 'least-response-time':
            return self.get_least_response_time(registrations)

   def get_random(self, registrations):
      return random.choice(registrations) or None
   
   def get_round_robin(self, registrations):
      return registrations.pop(0) or None
   
   def get_least_response_time(self, registrations):
      registration_chosen = None
      response_time_chosen = float('inf')
      for registration in registrations:
         response_time, status_code = self.ping_endpoint(registration)
         if status_code == 200:
            if response_time < response_time_chosen:
               response_time_chosen = response_time
               registration_chosen = registration
      return registration_chosen

   
   def ping_endpoint(self, registration):
      try:
         start_time = time.time() 
         response = requests.get(f'{registration.to_base_url()}')
         end_time = time.time()
         response_time = end_time - start_time
         return response_time, response.status_code
      except requests.exceptions.RequestException:
         return float('inf'), 500
