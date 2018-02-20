FROM ubuntu:16.04

LABEL manteiner = "Paco Ocampo - Centraal Academy paco@centraal.com"

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    libpq-dev \
    python-pip \
    python2.7 \
    python2.7-dev \
    && apt-get autoremove \
    && apt-get clean

    
CMD ["/usr/bin/python", "-m", "SimpleHTTPServer", "80"]

EXPOSE 80


