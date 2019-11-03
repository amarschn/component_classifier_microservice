FROM ubuntu:16.04

# Get needed software updates to install freecad and cadquery
RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:freecad-maintainers/freecad-stable && \
    apt-get update && apt-get install -y freecad
RUN apt-get install -y python-pip
RUN apt-get install -y libgraphicsmagick1-dev libmagickcore-dev libmagickcore-6.q16-2 libmagickcore-6.q16-2-extra
# Install the old cadquery which works with freecad, this is necessary because the newer
# cadquery's implementation of toSvg() is extremely slow
# RUN pip install Wand
# RUN pip install cadquery
# Copy over the requirements.txt file and install all requirements. Make this separate from other copying so that
# requirements aren't reinstalled every time there is a code change
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Make the folder that will store the source code in the Docker image
RUN mkdir /app

# Pass in a directory path, that will define the path at which future commands
# are run
WORKDIR /app

# Copy all files to the working directory in the container
COPY . .

ENV FLASK_APP app.py

# Pass in a key and a value, attaching arbitrary metadata to the image
LABEL maintainer="EG <eg@enclosuregenerator.com>" \
      version="1.0"

# Defines the default command which will be executed once the docker image is run
# CMD flask run --host=0.0.0.0 --port=5000
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:5000", "app:app"]