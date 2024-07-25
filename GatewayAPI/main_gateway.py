from globals_gateway import app,api,PORT,HOST
from gateway import GatewayResource
from flask import render_template,request,redirect,url_for, current_user,is_safe_url,LoginForm
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


def loggin_required(f:Callable)->Callable:
   @wraps(f)
   def wrapper(*args, **kwargs):
      if current_user.is_authenticated:
         return f(*args, **kwargs)
      
      return redirect(url_for(endpoint='login', next_url=request.url))
   
   return wrapper

api.add_resource(GatewayResource,'/citybreak')


req_mapping = {'GET': Get, 'POST': Post, 'PUT': Put, 'DELETE': Delete}

@loggin_required
@app.route('/events', methods=['POST', 'PUT', 'DELETE'])
def events():
   return proxy_request(request, globals_gateway.EVENT_API_URL)


@loggin_required
@app.route('/weather', methods=['POST', 'PUT', 'DELETE'])
def weather():
   return proxy_request(request, globals_gateway.WEATHER_API_URL)


def proxy_request(request, target_url):
   req = req_mapping[request.method]
   kwargs = {'params' : request.args, 'url': target_url} 
   if request.method in ['POST', 'PUT']:
      kwargs['data'] = dict(request.form)
   print(f'kwargs: {kwargs}')
   response=req(**kwargs).json()
   return json.dumps(response)



@app.route('/login', methods=['GET', 'POST'])
def login():
   next_url = request.args.get('next_url') or '/index'
   if not is_safe_url(next_url):
      return 'Bad URL', 400
   
   form = LoginForm(request.form)
   if request.method == 'POST' and form.validate():
      pass
   else:
      return render_template('login.html', form=form, next_url=next_url)








if __name__ == '__main__':
   app.run(host=HOST,port=PORT, debug=True)   


