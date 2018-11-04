# Copyright 2018 Christopher M. Boyer
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

echo "
                            _________
                           /         /.
    .--------------.       /_________/ |
   /              / |      |         | |
  /+=============+\ |      | |====|  | |
  || $ run test  || |      |         | |
  ||             || |      | |====|  | |
  ||             || |      |   ___   | |
  ||             || |      |  |166|  | |
  ||             ||/@@@    |   ---   | |
  \+=============+/    @   |_________|./.
                      @          ..  ....'
  ...................@     __.'.'  ''
 /ooooooooooooooooo//     ///
/.................//     /_/
-------------------

"

pip list

python -m unittest discover test 2>&1 | tee unit_out.txt
if cat unit_out.txt| grep 'FAILED'
then
    rm unit_out.txt
    exit 1
fi
rm unit_out.txt


python -m unittest discover e2e 2>&1 | tee e2e_out.txt
if cat e2e_out.txt| grep 'FAILED'
then
    rm e2e_out.txt
    exit 1
fi
rm e2e_out.txt


echo "
 ▄▄▄· ▄▄▄· .▄▄ · .▄▄ · ▄▄▄ .·▄▄▄▄  ▄▄
▐█ ▄█▐█ ▀█ ▐█ ▀. ▐█ ▀. ▀▄.▀·██▪ ██ ██▌
 ██▀·▄█▀▀█ ▄▀▀▀█▄▄▀▀▀█▄▐▀▀▪▄▐█· ▐█▌▐█·
▐█▪·•▐█ ▪▐▌▐█▄▪▐█▐█▄▪▐█▐█▄▄▌██. ██ .▀
.▀    ▀  ▀  ▀▀▀▀  ▀▀▀▀  ▀▀▀ ▀▀▀▀▀•  ▀
"