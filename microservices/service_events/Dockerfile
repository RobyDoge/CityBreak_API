FROM microskel

ADD . /opt/event
WORKDIR /opt/event

RUN pip install -r requirements.txt

CMD ["python", "service_events.py"]
