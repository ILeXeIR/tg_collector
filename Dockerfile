FROM python:3.11-alpine
LABEL maintainer="Alexander Petukhov <al.v.petukhov@gmail.com>"

WORKDIR /opt/tg_collector

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

CMD python3 main.py