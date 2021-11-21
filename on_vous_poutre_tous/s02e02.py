#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# s02e02.py
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

remote_id1 = int(input('Remote 1 id ? '))
remote_id2 = int(input('Remote 2 id ? '))

C = CubeController()
C.blit()
R1 = RemoteController(remote_id1)
R2 = RemoteController(remote_id2)

pos1 = np.array([0, 0, 0])
pos2 = np.array([0, 0, 0])
c1 = [255, 0, 0]
c2 = [0, 0, 255]

def move(c, pos, other_pos, other_c, *dpos):
    if np.all(pos == other_pos):
        C[tuple(pos)] = other_c
    else:
        C[tuple(pos)] = [0]*3
    pos += dpos
    pos %= 4
    if np.all(pos == other_pos):
        C[tuple(pos)] = [c[i] + other_c[i] for i in range(3)]
    else:
        C[tuple(pos)] = c
    return pos

def process_inputs(pos, v, c, other_pos, other_c):
    new_pos = pos
    if v & 2**0: new_pos = move(c, pos, other_pos, other_c, 1, 0, 0)
    if v & 2**1: new_pos = move(c, pos, other_pos, other_c, 0, 1, 0)
    if v & 2**2: new_pos = move(c, pos, other_pos, other_c, 0, 0, 1)
    if v & 2**3: new_pos = move(c, pos, other_pos, other_c, -1, 0, 0)
    if v & 2**4: new_pos = move(c, pos, other_pos, other_c, 0, -1, 0)
    if v & 2**5: new_pos = move(c, pos, other_pos, other_c, 0, 0, -1)
    if v & 2**6: return pos, True
    return new_pos, False

quit = False
while not quit:
    for v in R1.recv():
        pos1, quit = process_inputs(pos1, v, c1, pos2, c2)
        if quit: break
    for v in R2.recv():
        pos2, quit = process_inputs(pos2, v, c2, pos1, c1)
        if quit: break

C.fill()
time.sleep(.1)
C.stop()
R1.stop()
R2.stop()
