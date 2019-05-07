# Copyright 2019 Christopher M. Boyer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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

