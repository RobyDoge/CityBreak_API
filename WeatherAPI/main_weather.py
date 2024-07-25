from globals_weather import app,db,api,PORT,HOST
from weather import WeatherResource
import os

db_host:str = os.environ.get('DB_HOST') or 'localhost:3306'
db_user:str = os.environ.get('DB_USER') or 'roby'
db_pw:str = os.environ.get('DB_PASSWORD') or '1234'
db_name:str = os.environ.get("DB_NAME") or 'citybreak'
PORT:int = int(os.environ.get('PORT') or 5002)
HOST:str = os.environ.get('HOST') or '127.0.0.1'


@app.route('/')
def index()->str:
   return ""


api.add_resource(WeatherResource, '/weather')

with app.app_context():
   db.create_all()


if __name__ == '__main__':
   print(f"DB URL: {db_host}")
   app.run(host=HOST,port=PORT, debug=True)   


