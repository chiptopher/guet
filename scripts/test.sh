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