#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# s02e01.py
#
# Copyright © 2021 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

import time
import numpy as np
from controllers import RemoteController, CubeController

remote_id = int(input('Remote id ? '))

C = CubeController()
C.blit()
R = RemoteController(remote_id)


position = np.array([0, 0, 0])
def move(*dpos):
    global position
    C[tuple(position)] = [0]*3
    position += dpos
    position %= 4
    C[tuple(position)] = [255]*3

quit = False
while not quit:
    for v in R.recv():
        if v & 2**0: move(1, 0, 0)
        if v & 2**1: move(0, 1, 0)
        if v & 2**2: move(0, 0, 1)
        if v & 2**3: move(-1, 0, 0)
        if v & 2**4: move(0, -1, 0)
        if v & 2**5: move(0, 0, -1)
        if v & 2**6:
            quit = True
            break

C.fill()
time.sleep(.1)
C.stop()
R.stop()





