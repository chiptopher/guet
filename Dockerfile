FROM python:3.7-buster
COPY . .
RUN python ./setup.py install

WORKDIR /root/test-env

