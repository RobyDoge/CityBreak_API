from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import *
from sqlalchemy import *

from microskel.db_module import Base


class EventModel(Base):
   __tablename__ = 'event'
   id = Column(Integer,primary_key=True)
   city = Column(String(128))
   date = Column(String(128))
   title = Column(String(128))
   description = Column(String(1024))

   def __init__(self, city, date, title, description):
      self.city = city
      self.date = date
      self.title = title
      self.description = description

   def to_dict(self):
      d = {}
      for k in self.__dict__.keys():
         if not '_state' in k:
            d[k] = self.__dict__[k]
      d['date'] = str(d['date'])
      return d


def configure_views(app):
   @app.route('/events/<city>', methods=['GET'])
   def get_events(city:str,db:SQLAlchemy ):
      try:
         event = db.session.query(EventModel).filter(EventModel.city == city).all()
      except NoResultFound as e:
         response = jsonify(status='No such city', context=city)
         response.status = '404'
         return response
      else:
         if not event:
            response = jsonify(status='No such city', context=city)
            response.status = '404'
            return response
         
         return [e.to_dict() for e in event], 200
   
   @app.route('/events', methods=['POST'])
   def create_event(request:Request, db:SQLAlchemy):
      try:
         event:EventModel = EventModel(city=request.form.get('city'),
                                 date=request.form.get('date'),
                                 title=request.form.get('title'),
                                 description=request.form.get('description'))
      except Exception as error:
         return f'{error}', 400
      else:
         db.session.add(event)
         db.session.commit()
         return str(event.id), 201
   
   @app.route('/events', methods=['PUT'])
   def update_event(request:Request, db:SQLAlchemy):
      try:
         id:int = int(request.form.get('id'))
         event:EventModel = db.session.query(EventModel).filter(EventModel.id == id).first()
      except Exception as error:
         return 'BAD REQUEST', 400
      else:
         event.city = request.form.get('city') or event.city
         event.date = request.form.get('date') or event.date
         event.title = request.form.get('title') or event.title
         event.description = request.form.get('description') or event.description
         db.session.commit()
         return 'OK', 200
   
   @app.route('/events', methods=['DELETE'])
   def delete_event(request:Request, db:SQLAlchemy):
      try:
         id:int = int(request.form.get('id'))
         event:EventModel = db.session.query(EventModel).filter(EventModel.id == id).first()
      except Exception as error:
         return 'BAD REQUEST', 400
      else:
         db.session.delete(event)
         db.session.commit()
         return 'OK', 200

      