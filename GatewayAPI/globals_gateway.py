from flask import Flask
from flask_restful import Api

app = Flask('gateway')
api = Api(app) 
EVENT_API_URL:str = 'http://localhost:5002/event'
WEATHER_API_URL:str  = 'http://localhost:5001/weather'