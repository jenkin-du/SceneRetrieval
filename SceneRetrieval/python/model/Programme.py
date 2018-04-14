# -*- coding:utf-8 -*-

import time


class Programme(object):

    _startTime = 0
    _stopTime = 0

    def start(self):
        self._startTime = int(round(time.time() * 1000))

    def stop(self):
        self._stopTime = time.time()
        self._stopTime = int(round(self._stopTime * 1000))
        dt = self._stopTime - self._startTime
        dt = dt / 1000.0
        print("successfully!"),
        print("executed time:"),
        print(bytes(dt))
