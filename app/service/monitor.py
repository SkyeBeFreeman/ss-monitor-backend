# encoding: utf-8


import subprocess
import time
from models.output import Output
from app import cfg, sched, user_list, db
from pymongo import DESCENDING
from dao import save


def start_watching():
    if cfg.get('other', 'is_watching') == '0':
        cfg.set('other', 'is_watching', '1')
        with open('config.ini', 'w+') as f:
            cfg.write(f)
        db['output'].create_index([("time", DESCENDING)], background=True)
        for user in user_list:
            result = subprocess.Popen(['sudo iptables -A OUTPUT -p tcp --sport ' + user.port], stdout=subprocess.PIPE,
                                      shell=True).communicate()
            stderr = result[1]
            if stderr is not None:
                print "start_watching error: " + stderr


@sched.interval_schedule(minutes=1)
def check_watching():
    if cfg.get('other', 'is_watching') == '1':
        result = subprocess.Popen(['sudo iptables -L -v -n -x'], stdout=subprocess.PIPE, shell=True).communicate()
        stdout = result[0]
        stderr = result[1]
        if stderr is None:
            try:
                # print stdout
                length = len(user_list)
                current_time = int(round(time.time() * 1000))
                result = stdout.split("\n")[-length - 1:-1]
                for i in range(length):
                    result[i] = Output(result[i].split()[-1].split(':')[1], result[i].split()[1], current_time)
                    save(result[i])
                # for item in result:
                #     print item
            except Exception, e:
                print str(e)
        else:
            print "check_watching error: " + stderr


def stop_watching():
    if cfg.get('other', 'is_watching') == '1':
        cfg.set('other', 'is_watching', '0')
        with open('config.ini', 'w+') as f:
            cfg.write(f)
            sched.unschedule_job(check_watching.job)
        for user in user_list:
            result = subprocess.Popen(['sudo iptables -D OUTPUT -p tcp --sport ' + user.port], stdout=subprocess.PIPE, shell=True).communicate()
            stderr = result[1]
            if stderr is not None:
                print "stop_watching error: " + stderr

