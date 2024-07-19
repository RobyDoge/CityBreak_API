from flask_sqlalchemy import SQLAlchemy 
from flask import Flask
from flask_restful import Api


app = Flask('event')
db_host:str = 'localhost:3306'
db_user:str = 'roby'
db_pw:str = '1234'
db_name:str = 'citybreak'
db_url:str = f"mysql://{db_user}:{db_pw}@{db_host}/{db_name}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db:SQLAlchemy = SQLAlchemy(app)
api = Api(app) 