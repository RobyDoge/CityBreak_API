FROM microskel

ADD . /opt/weather
WORKDIR /opt/weather

RUN pip install -r requirements.txt

CMD ["python", "service_weather.py"]
