FROM ubuntu:16.04
EXPOSE 8000
RUN apt-get update
RUN apt-get install -y python-django
RUN apt-get install -y wget
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.1.0/dockerize-linux-amd64-v0.1.0.tar.gz
RUN tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.1.0.tar.gz
RUN apt-get install -y python-pip
RUN mkdir -p /StickerConsole
ADD . /StickerConsole
ADD requirements/requirements.txt /data/requirements.txt
RUN pip install --quiet -r /data/requirements.txt
