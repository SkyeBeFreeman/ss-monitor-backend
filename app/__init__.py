#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from configparser import ConfigParser
from models.user import User
import json
import pymongo

class MyConfigParser(ConfigParser):
    def optionxform(self, optionstr):
        return optionstr


app = Flask(__name__)

# 读取配置
cfg = MyConfigParser()
cfg.read('config.ini')
# print(cfg)
for k, v in cfg.items('web'):
    if k == 'DEBUG':
        if (v == 'True'):
            app.config[k] = True
        else:
            app.config[k] = False
    else:
        app.config[k] = v

# print(app.config)
CORS(app)

# MongoDB
client = pymongo.MongoClient(host=cfg.get('db', 'hostname'), port=cfg.getint('db', 'port'))
db = client[cfg.get('db', 'dbname')]
# collection = db['user']

# 数据初始化
user_list = []

with open(cfg.get('other', 'infofilepath'), "r") as load_f:
    load_dict = json.load(load_f)['port_password']
    for key in load_dict:
        user = User(load_dict[key], key)
        user_list.append(user)
        print(user)

# api的业务逻辑
from . import restful, service

# service.monitor.start_watching(user_list)


