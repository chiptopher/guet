FROM python:3.7-buster
COPY . .
RUN python ./setup.py install

WORKDIR /
RUN git clone https://github.com/wolfcw/libfaketime.git
WORKDIR /libfaketime/src
RUN make install

WORKDIR /root/test-env

