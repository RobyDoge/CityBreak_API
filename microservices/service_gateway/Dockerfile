FROM microskel

ADD . /opt/service_gateway
WORKDIR /opt/service_gateway

ENV RETRY_STRATEGY=EXPONENTIAL_BACKOFF

RUN pip install -r requirements.txt
CMD ["python", "service_gateway.py"]