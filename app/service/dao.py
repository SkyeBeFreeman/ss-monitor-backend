# encoding: utf-8


from app import db, user_list, user_data, sched
from pymongo import DESCENDING
from models.output import Output
import logging
logging.basicConfig()

USER_DATA_MAX_LENGTH = 24 * 60 + 1
# USER_DATA_MAX_LENGTH = 5


def init_user_data():
    for user in user_list:
        cursor = db['output'].find({'port': user.port}).sort('time', DESCENDING)
        count = db['output'].count_documents({'port': user.port})
        if count <= USER_DATA_MAX_LENGTH:
            for item in cursor:
                user_data[user.port].insert(0, dict_2_output(item))
        else:
            cnt = 0;
            for item in cursor:
                user_data[user.port].insert(0, dict_2_output(item))
                cnt += 1
                if cnt == USER_DATA_MAX_LENGTH:
                    break
    print_user_data()


def save(data, col='output'):
    db[col].insert_one(data.__dict__)
    if is_oversize(data.port):
        user_data[data.port].pop(0)
    user_data[data.port].append(data)


def delete_all(col='output'):
    db[col].delete_many({})


def is_oversize(port):
    temp_len = len(user_data[port])
    if temp_len <= USER_DATA_MAX_LENGTH:
        return False
    else:
        return True


@sched.cron_schedule(day_of_week=0)
def clean_mongodb():
    db['output'].delete_many({})
    print_user_data()
    for user in user_list:
        db['output'].insert_many(map(output_2_dict, user_data[user.port]))


def output_2_dict(data):
    return data.__dict__


def dict_2_output(data):
    return Output(data['port'], data['count'], data['time'])


def print_user_data():
    for user in user_list:
        for item in user_data[user.port]:
            print item


def return_form_data():
    data = []
    for user in user_list:
        temp = []
        length = len(user_data[user.port])
        for i in range(length - 1):
            temp.append([
                int(user_data[user.port][i + 1].count.encode('utf-8')) - int(user_data[user.port][i].count.encode('utf-8')),
                long(user_data[user.port][i + 1].time.encode('utf-8'))
            ])
        data.append({
            "name": user.name,
            "port": user.port,
            "content": temp
        })
    return data

