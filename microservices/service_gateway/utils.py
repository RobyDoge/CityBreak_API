
from requests import get as Get
from requests import post as Post
from requests import put as Put
from requests import delete as Delete
import json

req_mapping = {
   'GET': Get,
   'POST': Post,
   'PUT': Put,
   'DELETE': Delete
}


def proxy_request(request, target_url):
   req = req_mapping[request.method]
   kwargs = {'params' : request.args, 'url': target_url} 
   if request.method in ['POST', 'PUT']:
      kwargs['data'] = dict(request.form)
   print(f'kwargs: {kwargs}')
   response=req(**kwargs).json()
   return json.dumps(response)   