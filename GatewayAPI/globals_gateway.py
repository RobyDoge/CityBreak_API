from flask import Flask
from flask_restful import Api
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask('gateway')

db_host:str = os.environ.get('DB_HOST') or 'localhost:3306'
db_user:str = os.environ.get('DB_USER') or 'roby'
db_pw:str = os.environ.get('DB_PASSWORD') or '1234'
PORT:int = int(os.environ.get('PORT') or 5002)
HOST:str = os.environ.get('HOST') or '127.0.0.1'
db_name:str = os.environ.get("DB_NAME") or 'citybreak'
db_url:str = f"mysql://{db_user}:{db_pw}@{db_host}/{db_name}"
app.secret_key='secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SESSION_TYPE'] = 'filesystem'
app.config['Session_Permanent'] = False
db:SQLAlchemy = SQLAlchemy(app)
api = Api(app) 
EVENT_API_URL:str= os.environ.get('EVENT_URL') or 'error'
WEATHER_API_URL:str  = os.environ.get('WEATHER_URL') or 'error'

if EVENT_API_URL == 'error' or WEATHER_API_URL == 'error':
   raise ValueError('Environment variables not set')

PORT:int = int(os.environ.get('PORT') or 5000)
HOST:str = os.environ.get('HOST') or '0.0.0.0'