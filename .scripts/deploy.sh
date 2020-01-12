#!/usr/bin/env bash

echo
echo This will commit to the production python package index.
echo If you are sure you want to do this, hit any button to
echo continue or Ctrl-C if you want to quit.
read varname
echo

rm -rf dist/

python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*