#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# s02e03.py
#
# Copyright © 2021 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

from controllers import RemoteController

remote_id = int(input('Remote id ? '))

R = RemoteController(remote_id)

quit = False
while not quit:
    for v in R.recv():
        if v & 2**0:
            R.send(1)
        if v & 2**1:
            R.send(2)
        if v & 2**2:
            R.send(4)
        if v & 2**6:
            quit = True
            break

