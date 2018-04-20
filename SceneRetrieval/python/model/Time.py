# -*- coding:utf-8 -*-

import time


class Time(object):
    _startTime = 0
    _stopTime = 0
    _description = ""

    def __init__(self, description=""):
            self._description = description

    def start(self):
        print("---------"+self._description + " start ----------")
        self._startTime = int(round(time.time() * 1000))

    def stop(self):
        self._stopTime = time.time()
        self._stopTime = int(round(self._stopTime * 1000))
        dt = self._stopTime - self._startTime
        dt = dt / 1000.0
        print("-------- stop "),
        print("executed time:"),
        print(bytes(dt)),
        print("--------")
