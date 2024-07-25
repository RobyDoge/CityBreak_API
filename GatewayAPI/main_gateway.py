from globals_gateway import app,api,PORT,HOST
from gateway import GatewayResource
from flask import render_template,request
import os
import globals_gateway
from requests import get as Get
from requests import post as Post
from requests import put as Put
from requests import delete as Delete
import json

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


api.add_resource(GatewayResource,'/citybreak')


req_mapping = {'GET': Get, 'POST': Post, 'PUT': Put, 'DELETE': Delete}


@app.route('/events', methods=['GET', 'POST', 'PUT', 'DELETE'])
def events():
   return proxy_request(request, globals_gateway.EVENT_API_URL)


@app.route('/weather', methods=['GET', 'POST', 'PUT', 'DELETE'])
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


if __name__ == '__main__':
   app.run(host=HOST,port=PORT, debug=True)   


