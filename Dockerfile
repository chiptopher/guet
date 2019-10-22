FROM python:3.7-alpine
COPY . .
RUN mkdir test-env
RUN python ./setup.py install

WORKDIR ./test-env

