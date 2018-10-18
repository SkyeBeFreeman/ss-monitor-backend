#!/usr/bin/env python
# -*- coding: utf-8 -*-


class User(object):

    def __init__(self, name, port):
        self.name = name
        self.port = port

    def __str__(self):
        return "name:{} - port:{}".format(self.name, self.port)
