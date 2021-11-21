#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# s01e03.py
#
# Copyright © 2021 Mathieu Gaborit (matael) <mathieu@matael.org>
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Mathieu (matael) Gaborit wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy me a beer or coffee in return
#

import time

from controllers import CubeController

c = CubeController()
position = tuple(map(int, input('give me a postition x y z: ').split()))
color = tuple(map(int, input('give me a color r g b: ').split()))
c[position] = color
input("Press key to stop")
c.stop()


