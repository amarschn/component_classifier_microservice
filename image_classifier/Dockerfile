FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY . .

ENV FLASK_APP app.py

LABEL maintainer="EG <eg@enclosuregenerator.com>" \
      version="1.0" 

# CMD python test.py
# Defines the default command which will be executed once the docker image is run
CMD flask run --host=0.0.0.0 --port=5000
# CMD python app.py