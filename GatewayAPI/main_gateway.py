from re import L
from globals_gateway import app,api,PORT,HOST,db
from gateway import GatewayResource
from flask import  render_template, request, redirect, url_for,Flask
from flask_login import current_user, login_user, UserMixin,LoginManager
from flask_restful import Resource
from wtforms import *
import os
import globals_gateway
from requests import get as Get
from requests import post as Post
from requests import put as Put
from requests import delete as Delete
import json
from typing import Callable
from functools import wraps

globals_gateway.EVENT_API_URL = os.environ.get('EVENT_URL') or 'error'
globals_gateway.WEATHER_API_URL  = os.environ.get('WEATHER_URL') or 'error'

if globals_gateway.EVENT_API_URL == 'error' or globals_gateway.WEATHER_API_URL == 'error':
   raise ValueError('Environment variables not set')

@app.route('/')
def index()->str:
   people =[
      {'first_name':'John', 'last_name':'Doe'},
      {'first_name':'Jane', 'last_name':'Doe'},
      {'first_name':'Jen', 'last_name':'Doe'},
      {'first_name':'Jill', 'last_name':'Doe'}

   ]
   return render_template('index.html',name = 'John Doe', people = people)

@app.route('/add_user')
def add_user():
   user = User(email='roby@gmail.com', password='1234', name='Roby')
   db.session.add(user)
   db.session.commit()

def loggin_required(f:Callable)->Callable:
   @wraps(f)
   def wrapper(*args, **kwargs):
      if current_user.is_authenticated:
         return f(*args, **kwargs)
      return redirect(url_for(endpoint='login', next_url=request.url))
   return wrapper


def proxy_request(request, target_url):
   req = req_mapping[request.method]
   kwargs = {'params' : request.args, 'url': target_url} 
   if request.method in ['POST', 'PUT']:
      kwargs['data'] = dict(request.form)
   print(f'kwargs: {kwargs}')
   response=req(**kwargs).json()
   return json.dumps(response)


class User(db.Model,UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   email = db.Column(db.String(100), unique=True)
   password = db.Column(db.String(100))
   name = db.Column(db.String(100))


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class LoginUser(UserMixin):
   def __init__(self,id):
      self.id=id

class LoginForm(Form):
   def check_existing(form,field):
      existing  = db.session.query(User).filter(User.email==field.data).first()
      if not existing:
         raise ValidationError('Email not found')         

   email = StringField('Email / User', validators=[validators.DataRequired('Email is required'),
                                                   validators.Email('Invalid email')])
   password = PasswordField('Password', validators=[validators.DataRequired('Password is required')])

def authenticate(email:str,password:str)->bool  :
   if not email or not password:
      return False
   result = db.session.query(User).filter(User.email==email).first()
   return result and result.password == password   


req_mapping = {'GET': Get, 'POST': Post, 'PUT': Put, 'DELETE': Delete}



@loggin_required
@app.route('/events', methods=['POST', 'PUT', 'DELETE'])
def events():
   return proxy_request(request, globals_gateway.EVENT_API_URL)


@loggin_required
@app.route('/weather', methods=['POST', 'PUT', 'DELETE'])
def weather():
   return proxy_request(request, globals_gateway.WEATHER_API_URL)




@app.route('/login', methods=['GET', 'POST'])
def login():
   next_url = request.args.get('next_url') or '/'
   # if not is_safe_url(next_url):
   #    return 'Bad URL', 400
   
   form = LoginForm(request.form)
   if request.method == 'POST' and form.validate():
      email = form.email.data
      password = form.password.data
      auth = authenticate(email, password)
      if not auth:
         form.password.errors = ['Invalid email or password']
         app.logger.error(f'Login invalid for {email} and {password}')
         return render_template(f'login.html', form=form, next_url=next_url)
      app.logger.error(f'Login invalid for {email} and {password}')
      login_user(LoginUser(email))
      #user = db.session.query(User).filter(User.email==email).first()
      
      return redirect(next_url)
   else:
      return render_template('login.html', form=form, next_url=next_url)


api.add_resource(GatewayResource,'/citybreak')

with app.app_context():
   db.create_all()

if __name__ == '__main__':

   app.run(host=HOST,port=PORT, debug=True)   


