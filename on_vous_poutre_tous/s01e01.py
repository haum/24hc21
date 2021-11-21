#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# s01e01.py
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
for i in range(10):
    c[0, 0, 0] = [255, 0, 0]
    time.sleep(.5)
    c[0, 0, 0] = [0, 0, 0]
    time.sleep(.5)

c.stop()



