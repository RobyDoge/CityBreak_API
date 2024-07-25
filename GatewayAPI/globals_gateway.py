from flask import Flask
from flask_restful import Api
import os


app = Flask('gateway')
api = Api(app) 
EVENT_API_URL:str= os.environ.get('EVENT_URL') or 'error'
WEATHER_API_URL:str  = os.environ.get('WEATHER_URL') or 'error'

if EVENT_API_URL == 'error' or WEATHER_API_URL == 'error':
   raise ValueError('Environment variables not set')

PORT:int = int(os.environ.get('PORT') or 5000)
HOST:str = os.environ.get('HOST') or '0.0.0.0'