from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import *
from sqlalchemy import *

from microskel.db_module import Base


class WeatherModel(Base):
   __tablename__ = 'weather'
   id = Column(Integer,primary_key=True)
   city = Column(String(128))
   date = Column(String(128))
   temperature = Column(Float)
   humidity = Column(Float)

   def __init__(self, city, date, temperature, humidity):
      self.city = city
      self.date = date
      self.temperature = temperature
      self.humidity = humidity

   def to_dict(self):
      d = {}
      for k in self.__dict__.keys():
         if not '_state' in k:
            d[k] = self.__dict__[k]
      d['date'] = str(d['date'])
      return d


def configure_views(app):
   @app.route('/weather/<city>', methods=['GET'])
   def get_weather_for_city(city:str,db:SQLAlchemy ):
      try:
         weather_list = db.session.query(WeatherModel).filter(WeatherModel.city == city).all()
      except NoResultFound as e:
         response = jsonify(status='No such city', context=city)
         response.status = '404'
         return response
      else:
         if not weather_list:
            response = jsonify(status='No such city', context=city)
            response.status = '404'
            return response
         
         return [e.to_dict() for e in weather_list], 200
   
   @app.route('/weather', methods=['POST'])
   def create_weather(request:Request, db:SQLAlchemy):
      try:
         weather:WeatherModel = WeatherModel(city=request.form.get('city'),
                                 date=request.form.get('date'),
                                 temperature=request.form.get('temperature'),
                                 humidity=request.form.get('humidity'))
      except Exception as error:
         return f'{error}', 400
      else:
         db.session.add(weather)
         db.session.commit()
         return str(weather.id), 201

   
   @app.route('/weather', methods=['PUT'])
   def update_weather(request:Request, db:SQLAlchemy):
      try:
         id:int = int(request.form.get('id'))
         weather:WeatherModel = db.session.query(WeatherModel).filter(WeatherModel.id == id).first()
      except Exception as error:
         return f'{error}', 400
      else:
         weather.city = request.form.get('city') or weather.city
         weather.date = request.form.get('date') or weather.date
         weather.temperature = request.form.get('temperature') or weather.temperature
         weather.humidity = request.form.get('humidity') or weather.humidity
         db.session.commit()
         return 'OK', 200

   @app.route('/weather', methods=['DELETE'])
   def delete_weather(request:Request, db:SQLAlchemy):
      try:
         id:int = int(request.form.get('id'))
         weather:WeatherModel = db.session.query(WeatherModel).filter(WeatherModel.id == id).first()
      except Exception as error:
         return f'{error}', 400
      else:
         db.session.delete(weather)
         db.session.commit()
         return 'OK', 200
      