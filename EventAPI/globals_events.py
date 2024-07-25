from flask_sqlalchemy import SQLAlchemy 
from flask import Flask
from flask_restful import Api
import os
import logging
from logging import FileHandler
import time

app = Flask('event')
db_host:str = os.environ.get('DB_HOST') or 'localhost:3306'
db_user:str = os.environ.get('DB_USER') or 'roby'
db_pw:str = os.environ.get('DB_PASSWORD') or '1234'
db_name:str = os.environ.get("DB_NAME") or 'citybreak'
PORT:int = int(os.environ.get('PORT') or 5002)
HOST:str = os.environ.get('HOST') or '127.0.0.1'
db_url:str = f"mysql://{db_user}:{db_pw}@{db_host}/{db_name}"

file_hander:FileHandler = logging.FileHandler('event.log')
app.logger.addHandler(file_hander)
app.logger.setLevel(logging.INFO)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url

time.sleep(20)

db:SQLAlchemy = SQLAlchemy(app)
api = Api(app)




