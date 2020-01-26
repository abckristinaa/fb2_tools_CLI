FROM ubuntu

WORKDIR /fb2tools

RUN apt-get update && apt-get install python3 -y

COPY requirements.txt .

RUN apt-get install python3-pip -y
RUN pip3 install -r requirements.txt

COPY digger.py .
COPY seeker.py .
COPY wiper.py .
COPY db_methods.py .
COPY config.ini .
