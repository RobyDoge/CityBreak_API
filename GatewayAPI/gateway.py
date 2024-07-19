from flask import request
from flask_restful import Resource
from typing import List,Tuple,Dict
import requests
from requests import Response

from utils import ReturnCode
from globals_gateway import WEATHER_API_URL,EVENT_API_URL


class GatewayResource(Resource):
   def get(self)->Tuple[Dict[str,List[Dict[str,str]]|str],int]:
      city:str|None = request.args.get('city')
      date:str|None = request.args.get('date')
      if not city or not date:
         return {},ReturnCode.BAD_REQUEST._value_
      
      params:Dict[str,str] = {'city':city,'date':date}

      weather_response:Response = requests.get(WEATHER_API_URL,params=params)
      event_response:Response = requests.get(EVENT_API_URL,params=params)

      if weather_response.status_code != ReturnCode.OK._value_ or event_response.status_code != ReturnCode.OK._value_:
         return {},ReturnCode.NOT_FOUND._value_
      
      weather_data:List[Dict[str,str]] = weather_response.json()
      event_data:List[Dict[str,str]] = event_response.json()

      response:Dict[str,List[Dict[str,str]]|str] = {'city':city,'date':date, 'weather':weather_data,'event':event_data}

      return response,ReturnCode.OK._value_

