from global_events import app,db,api
from event import EventResource



@app.route('/')
def index()->str:
   return """
   <html>
      <body>
         <strong> Hello, World! </strong>
      </body>
   </html>
   """

api.add_resource(EventResource,'/event')

with app.app_context():
   db.create_all()


if __name__ == '__main__':
   app.run(host='0.0.0.0',port=5000, debug=True)   


