#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# tron.py
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

remote_id1, remote_id2 = map(int, input('Enter IDs for remotes 1 & 2: ').split())

C = CubeController()
C.blit()
R1 = RemoteController(remote_id1)
R2 = RemoteController(remote_id2)

pos1 = np.array([0]*3)
pos2 = np.array([3]*3)
player_info = {1: [252, 116, 30], 2: [73, 162, 178]}

C[tuple(pos1)] = player_info[1]
C[tuple(pos2)] = player_info[2]

cubemap = np.zeros((4, 4, 4), dtype=int)

def move(player, pos, *dpos):
    other_player = 1 if player == 2 else 2
    pos += dpos
    pos %= 4
    if cubemap[tuple(pos)]:
        return pos, False
    C[tuple(pos)] = player_info[player]
    cubemap[tuple(pos)] = 1
    return pos, True

def process_inputs(player, pos, v):
    alive = True
    new_pos = pos
    if v & 2**0: new_pos, alive = move(player, pos, 1, 0, 0)
    if v & 2**1: new_pos, alive = move(player, pos, 0, 1, 0)
    if v & 2**2: new_pos, alive = move(player, pos, 0, 0, 1)
    if v & 2**3: new_pos, alive = move(player, pos, -1, 0, 0)
    if v & 2**4: new_pos, alive = move(player, pos, 0, -1, 0)
    if v & 2**5: new_pos, alive = move(player, pos, 0, 0, -1)
    if v & 2**6: return pos, True, True
    return new_pos, alive, False

quit = False
alive1, alive2 = True, True
while not quit and alive1 and alive2:
    for v in R1.recv():
        pos1, alive1, quit = process_inputs(1, pos1, v)
        if quit or not alive1: break
    for v in R2.recv():
        pos2, alive2, quit = process_inputs(2, pos2, v)
        if quit or not alive2: break

if not alive1 or not alive2:
    c = player_info[1] if alive2 else player_info[2]
    pos = tuple(pos1 if alive2 else pos2)
    for i in range(3):
        d = 0.4*i
        C[pos] = [0]*3
        time.sleep(d)
        C[pos] = c
        time.sleep(d)
        C[pos] = [0]*3
        time.sleep(d)
        C[pos] = player_info[cubemap[pos]]
        time.sleep(d)

C.fill()
time.sleep(.1)
C.stop()
R1.stop()
R2.stop()
