# encoding: utf-8


from flask import Flask
from flask_cors import CORS
from configparser import ConfigParser
from models.user import User
from apscheduler.scheduler import Scheduler
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
        if v == 'True':
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

# 数据初始化
user_list = []
user_data = {}

with open(cfg.get('other', 'info_file_path'), "r") as load_f:
    load_dict = json.load(load_f)['port_password']
    for key in load_dict:
        user = User(load_dict[key], key)
        user_list.append(user)
        user_data[user.port] = []
        # print(user)

sched = Scheduler()
sched.start()

import restful, service
service.dao.init_user_data()
service.monitor.start_watching()


