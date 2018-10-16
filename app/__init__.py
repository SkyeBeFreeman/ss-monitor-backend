#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from configparser import ConfigParser
import json
import pymongo

class MyConfigParser(ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

app = Flask(__name__)

# 读取配置
cfg = MyConfigParser()
cfg.read('config.ini')
# print(cfg.items('web'))
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
collection = db['user']

# 数据初始化
collection.delete_many({})

with open(cfg.get('other', 'infofilepath'), "r") as load_f:
    load_dict = json.load(load_f)['port_password']
    for key in load_dict:
        user = {
            'name': load_dict[key], 
            'port': key            
        }
        result = collection.insert_one(user)
        # print(result)

# api的业务逻辑
import restful
