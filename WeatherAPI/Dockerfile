FROM python

ENV DB_HOST=localhost
ENV DB_USER=roby
ENV DB_PASSWORD=1234
ENV DB_NAME=events
ENV DB_PORT=5000
ENV HOST = 0.0.0.0

ADD . /opt/weather
WORKDIR /opt/weather

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "main_weather.py"]
