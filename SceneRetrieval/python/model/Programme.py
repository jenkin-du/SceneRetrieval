# -*- coding:utf-8 -*-

import time


class Programme(object):

    startTime = 0
    stopTime = 0

    def start(self):
        self.startTime = int(round(time.time() * 1000))

    def stop(self):
        self.stopTime = time.time()
        self.stopTime = int(round(self.stopTime * 1000))
        dt = self.stopTime - self.startTime
        dt = dt / 1000.0
        print("successfully!"),
        print("executed time:"),
        print(bytes(dt))
