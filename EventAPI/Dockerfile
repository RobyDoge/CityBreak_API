FROM python

ENV DB_HOST=localhost
ENV DB_USER=roby
ENV DB_PASSWORD=1234
ENV DB_NAME=events
ENV DB_PORT=5000
ENV HOST = 0.0.0.0

ADD . /opt/event
WORKDIR /opt/event

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "main_event.py"]
