#!/bin/sh

docker build . -t guettest:0.0.1
id=$(docker run -d -t guettest:0.0.1)
docker exec -it $id /bin/bash
