FROM ubuntu:20.04

EXPOSE 5000
WORKDIR /app

ENV FLASK_DEBUG=0

RUN apt-get update -y && \
    apt-get install -y python3-pip

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3" ]

CMD [ "run.py" ]