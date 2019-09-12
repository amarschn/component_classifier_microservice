# Base your image on a base image
FROM python:2.7-alpine

# Make the folder that will store the source code in the Docker image
RUN mkdir /app

# Pass in a directory path, that will define the path at which future commands
# are run
WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

# Copy all files to the working directory in the container
COPY . .

# Pass in a key and a value, attaching arbitrary metadata to the image
LABEL maintainer="EG <eg@enclosuregenerator.com>" \
      version="1.0"

# Defines the default command which will be executed once the docker image is run
CMD flask run --host=0.0.0.0 --port=8000