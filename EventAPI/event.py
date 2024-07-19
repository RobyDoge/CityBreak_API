from flask import request
from flask_restful import Resource
from typing import List,Tuple,Dict,Any
from datetime import date as Date

from utils import str_to_date,ReturnCode
from globals_events import db


class EventResource(Resource):
   def get(self)->Tuple[List[Dict[str,str]],int]:
      city:str|None = request.args.get('city')
      date:Date|None = str_to_date(request.args.get('date'))   

      conditions:Dict[str,Any] = {}
      
      if city:
         conditions['city'] = city
      if date:
         conditions['date'] = date
      
      events:List['EventModel'] = filter_events(conditions)
      if not events:
         return [],ReturnCode.NO_CONTENT._value_
      return [e.to_dict() for e in events],ReturnCode.OK._value_


   def post(self)->int:
      city:str|None = request.args.get('city')
      date:Date|None = str_to_date(request.args.get('date'))
      title:str|None = request.args.get('title')
      description:str|None = request.args.get('description')
      aux:str|None = request.args.get('price')
      price:float|None = float(aux) if aux else None
      category:str|None = request.args.get('category')
      weather_recommandation:str|None = request.args.get('weather_recommandation')
      location:str|None = request.args.get('location')

      if price and price < 0:
         return ReturnCode.BAD_REQUEST._value_
      if not all([city,date,title,description,price,category,weather_recommandation,location]):
         return ReturnCode.BAD_REQUEST._value_

      e:EventModel = EventModel(city=city,date=date,title=title,
                                description=description,
                                price=price,category=category,
                                weather_recommandation=weather_recommandation,
                                location=location) #type: ignore
      
      db.session.add(e)
      db.session.commit()
      return ReturnCode.CREATED._value_


   def put(self)->int:
      id:int = int(request.args.get('id') or -1)
      if id < 0:
         return ReturnCode.BAD_REQUEST._value_

      event:EventModel = filter_events({'id':id})[0]
      
      event.city = request.args.get('city') or event.city
      event.date = str_to_date(request.args.get('date')) or event.date
      event.title = request.args.get('title') or event.title
      event.description = request.args.get('description') or event.description

      db.session.commit()
      return ReturnCode.OK._value_

   def delete(self)->int:
      id:int = int(request.args.get('id') or -1)
      if id < 0:
         return ReturnCode.BAD_REQUEST._value_
      
      event:EventModel = filter_events({'id':id})[0]
      event.state = False

      db.session.commit()
      return ReturnCode.OK._value_


class EventModel(db.Model):
   __tablename__ = 'event'

   id:int = db.Column(db.Integer,primary_key=True)
   city:str = db.Column(db.String(128))
   date:Date = db.Column(db.Date)
   title:str = db.Column(db.String(128))
   description:str = db.Column(db.String(1024))
   state:bool  = db.Column(db.Boolean,default=True)
   price:float  = db.Column(db.Float,default=-1.0)
   category: str = db.Column(db.String(128))
   weather_recommandation:str = db.Column(db.String(128))
   location:str = db.Column(db.String(128))
   

   def to_dict(self)->Dict[str,str]:
      d:Dict[str,str] = {}
      for k in self.__dict__.keys():
         if not '_state' in k:
            d[k] = self.__dict__[k]
      d['date'] = str(d['date'])
      return d
   

#utils
def filter_events(filter_criteria:Dict[str,Any])->List['EventModel']:
      if not filter_criteria:
            return db.session.query(EventModel).all()
      attributa_value:List[Any] = []
      for criteria in filter_criteria:
            attributa_value.append(getattr(EventModel,criteria) == filter_criteria[criteria])
      if 'state' not in filter_criteria:
         attributa_value.append(EventModel.state == True)
      return db.session.query(EventModel).filter(*attributa_value).all()