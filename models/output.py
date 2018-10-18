#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Output(object):

    def __init__(self, port, count, time):
        self.port = port
        self.count = count
        self.time = time

    def __str__(self):
        return "port:{0} - count:{1} - time:{2}".format(self.port, self.count, self.time)