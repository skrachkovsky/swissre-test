FROM python:3.10-alpine

RUN apk update && apk add openssh git
WORKDIR /application
COPY ./ .
RUN pip install -r requirements.txt
ENV PYTHONPATH="$PYTHONPATH:/application"
