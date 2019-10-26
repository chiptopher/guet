FROM python:3.7-alpine
COPY . .
RUN python ./setup.py install

RUN apk update && apk add git

WORKDIR ./root/test-env

