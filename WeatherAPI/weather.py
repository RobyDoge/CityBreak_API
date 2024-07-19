from datetime import date as Date
from flask import request
from flask_restful import Resource
from typing import List,Dict,Tuple,Any
from sqlalchemy import and_

from utils import str_to_date, ReturnCode
from globals_weather import db


class WeatherResource(Resource):
   def get(self)->Tuple[List[Dict[str,str]],int]:
      city:str|None = request.args.get('city') or None
      date:Date|None = str_to_date(request.args.get('date'))
      
      conditions:Dict[str,Any] = {}
      if city:
         conditions['city'] = city
      if date:
         conditions['date'] = date
      weather:List['WeatherModel'] = filter_weather(conditions)
      if not weather:
         return [],ReturnCode.NO_CONTENT._value_
      return [w.to_dict() for w in weather],ReturnCode.OK._value_

   def post(self)->int:
      city:str|None = request.args.get('city')
      date:Date|None = str_to_date(request.args.get('date'))
      aux:str|None = request.args.get('temperature')
      temperature:float|None = float(aux) if aux else None
      aux = request.args.get('humidity')
      humidity:float|None = float(aux) if aux else None
      description:str = request.args.get('description') or 'Unknown'
      
      if (humidity and humidity<0) or (temperature and temperature<0):
         return ReturnCode.BAD_REQUEST._value_
      if not all([city,date,description]):
         return ReturnCode.BAD_REQUEST._value_
      
      w = WeatherModel(city=city,date=date,
                       temperature=temperature,
                       humidity=humidity,
                       description=description) #type: ignore
      
      db.session.add(w)
      db.session.commit()
      return ReturnCode.CREATED._value_

   def put(self)->int:
      id:int|None = int(request.args.get('id') or -1)
      if id<0:
         return ReturnCode.BAD_REQUEST._value_

      weather:WeatherModel = filter_weather({'id':id})[0]
      
      weather.city = request.args.get('city') or weather.city
      weather.date = str_to_date(request.args.get('date')) or weather.date
      aux: str|None = request.args.get('temperature')
      weather.temperature = float(aux) if aux else weather.temperature
      aux = request.args.get('humidity')
      weather.humidity = float(aux) if aux else weather.humidity
      weather.description = request.args.get('description') or weather.description

      db.session.commit()
      return ReturnCode.OK._value_

   def delete(self)->ReturnCode:
      id:int|None = int(request.args.get('id') or -1)
      if id<0:
         return ReturnCode.BAD_REQUEST
      
      weather:WeatherModel = filter_weather({'id':id})[0]
      weather.state = False

      db.session.commit()
      return ReturnCode.OK
      

class WeatherModel(db.Model):

   __tablename__ = 'weather'

   id:int = db.Column(db.Integer,primary_key=True)
   city:str = db.Column(db.String(128))
   date:Date = db.Column(db.Date)
   temperature:float = db.Column(db.Float)
   humidity:float = db.Column(db.Float)
   description:str = db.Column(db.String(1024))
   state:bool = db.Column(db.Boolean,default=True)


   def to_dict(self)->Dict[str,str]:
      d:Dict[str,str] = {}
      for k in self.__dict__.keys():
         if not '_state' in k:
            d[k] = self.__dict__[k]
      d['date'] = str(d['date'])
      return d
   

#utils
def filter_weather(filter_criteria:Dict[str,Any])->List['WeatherModel']:
   if not filter_criteria:
      return db.session.query(WeatherModel).all()
   
   attributa_value:List[Any] = []
   for criteria in filter_criteria:
         attributa_value.append(getattr(WeatherModel,criteria) == filter_criteria[criteria])
   if 'state' not in filter_criteria:
      attributa_value.append(WeatherModel.state == True)


   
   aux = db.session.query(WeatherModel).filter(and_(*attributa_value)).all()
   return aux
