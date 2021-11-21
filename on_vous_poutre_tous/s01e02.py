#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# s01e02.py
#
# Copyright © 2021 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

from controllers import CubeController

c = CubeController()
c.autoblit = False

c.fill([255]*3)
for i in range(4):
    c[i, i, i] = [255, 0, 0]

# blues
for i in range(3):
    c[1+i, i, i] = [0, 0, 255]
    c[i, 1+i, i] = [0, 0, 255]
    c[i, i, 1+i] = [0, 0, 255]

# green
for i in range(3):
    c[i, 1+i, 1+i] = [0, 255, 0]
    c[1+i, i, 1+i] = [0, 255, 0]
    c[1+i, 1+i, i] = [0, 255, 0]

# magenta
for i in range(2):
    c[2+i, i, i] = [255, 0, 255]
    c[i, 2+i, i] = [255, 0, 255]
    c[i, i, 2+i] = [255, 0, 255]

# cyan
for i in range(2):
    c[i, 2+i, 2+i] = [0, 255, 255]
    c[2+i, i, 2+i] = [0, 255, 255]
    c[2+i, 2+i, i] = [0, 255, 255]

# yellow
for i in range(2):
    c[i, 2+i, 1+i] = [255, 255, 0]
    c[i, 1+i, 2+i] = [255, 255, 0]
    c[2+i, i, 1+i] = [255, 255, 0]
    c[1+i, i, 2+i] = [255, 255, 0]
    c[2+i, 1+i, i] = [255, 255, 0]
    c[1+i, 2+i, i] = [255, 255, 0]

c.blit()
input("Press key to stop")
c.stop()



