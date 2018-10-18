import subprocess
import time
from models.output import Output
from app import cfg


def start_watching(user_list):
    if (cfg.get('other', 'is_watching') == '0'):
        cfg.set('other', 'is_watching', '1')
        with open('config.ini', 'w+') as f:
            cfg.write(f)
        for user in user_list:
            result = subprocess.Popen(['sudo iptables -A OUTPUT -p tcp --sport ' + user.port], stdout=subprocess.PIPE,
                                      shell=True).communicate()
            stderr = result[1]
            if stderr is not None:
                print "start_watching error: " + stderr


def check_watching(user_list):
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
            for item in result:
                print item
        except:
            print "Check_watching Error"
    else:
        print "check_watching error: "+ stderr


def stop_watching(user_list):
    if (cfg.get('other', 'is_watching') == '1'):
        cfg.set('other', 'is_watching', '0')
        with open('config.ini', 'w+') as f:
            cfg.write(f)
        for user in user_list:
            result = subprocess.Popen(['sudo iptables -D OUTPUT -p tcp --sport ' + user.port], stdout=subprocess.PIPE, shell=True).communicate()
            stderr = result[1]
            if stderr is not None:
                print "stop_watching error: " + stderr

