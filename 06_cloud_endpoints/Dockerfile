FROM python:3

LABEL manteiner = "Paco Ocampo - Centraal Academy paco@centraal.com"

RUN apt-get update && \
    apt-get install -y python3 python-pip && \
    apt-get clean && \
    rm /var/lib/apt/lists/*_* 

RUN mkdir /application

WORKDIR /application

COPY ./config/requirements.txt /application/

RUN pip3 install -r requirements.txt

COPY ./src /application/

ENTRYPOINT ["gunicorn", "-b", ":8000", "demo.wsgi"]

EXPOSE 8000
