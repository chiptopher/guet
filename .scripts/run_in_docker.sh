#!/bin/sh

set -e

source ./venv/bin/activate

python3 -m unittest discover test

rm -rf guet.egg-info/
rm -rf build/
rm -rf dist/

docker build . -t guettest:0.0.1
id=$(docker run -d -t guettest:0.0.1)
docker exec -it $id /bin/bash
