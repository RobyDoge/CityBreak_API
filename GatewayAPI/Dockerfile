FROM python

ENV WEATHER_URL=localhost
ENV EVENT_URL=localhost
ENV DB_PORT=5000
ENV HOST = 0.0.0.0

ADD . /opt/gateway
WORKDIR /opt/gateway

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "main_gateway.py"]
