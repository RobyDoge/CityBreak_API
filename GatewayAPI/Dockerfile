FROM python

ENV WEATHER_URL=localhost
ENV EVENT_URL=localhost
ENV DB_PORT=5000
ENV HOST = 0.0.0.0
ENV DB_HOST=localhost
ENV DB_USER=auth
ENV DB_PASSWORD=1234
ENV DB_NAME=auth

ADD . /opt/gateway
WORKDIR /opt/gateway

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "main_gateway.py"]
