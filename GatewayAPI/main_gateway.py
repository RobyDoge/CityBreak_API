from globals_gateway import app,api
from gateway import GatewayResource



@app.route('/')
def index()->str:
   return """
   <html>
      <body>
         <strong> Hello, World! </strong>
      </body>
   </html>
   """


api.add_resource(GatewayResource,'/gateway')


if __name__ == '__main__':
   app.run(host='0.0.0.0',port=5000, debug=True)   


