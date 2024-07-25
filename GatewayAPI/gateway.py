from flask import request
from flask_restful import Resource
from typing import List,Tuple,Dict
import requests
from requests import Response

from utils import ReturnCode
from globals_gateway import WEATHER_API_URL,EVENT_API_URL


class GatewayResource(Resource):
   def get(self)->Tuple[Dict[str,List[Dict[str,str]]|str]|str,int]:
      city:str|None = request.args.get('city')
      date:str|None = request.args.get('date')
      if not city or not date:
         return 'Inavlid request, missing argument',ReturnCode.BAD_REQUEST._value_
      
      params:Dict[str,str] = {'city':city,'date':date}

      weather_r:Response = requests.get(f'{WEATHER_API_URL}?city={city}&date={date}',verify=False)
      event_r:Response = requests.get(f'{EVENT_API_URL}?city={city}&date={date}',verify=False)

      if weather_r.status_code == ReturnCode.OK._value_ or event_r.status_code == ReturnCode.OK._value_:
         weather_data:List[Dict[str,str]] = weather_r.json()
         event_data:List[Dict[str,str]] = event_r.json()
         return {'city':city,'date':date, 'weather':weather_data,'event':event_data},ReturnCode.OK._value_


      if weather_r.status_code == ReturnCode.NO_CONTENT._value_ or event_r.status_code == ReturnCode.NO_CONTENT._value_:
         return {},ReturnCode.NO_CONTENT._value_
      
      return {},ReturnCode.NOT_FOUND._value_

   def post(self):
      pass
      

