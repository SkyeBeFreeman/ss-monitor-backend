# encoding: utf-8


from app import app, service, user_data
from flask import jsonify


@app.route('/api/start_watching', methods=['GET'])
def start_watching():
    service.monitor.start_watching()
    return "start_watching"


@app.route('/api/check_watching', methods=['GET'])
def check_watching():
    service.monitor.check_watching()
    return "check_watching"


@app.route('/api/stop_watching', methods=['GET'])
def stop_watching():
    service.monitor.stop_watching()
    return "stop_watching"


# @app.route('/api/delete_all', methods=['GET'])
def delete_all():
    service.dao.delete_all()
    return "delete_all"


@app.route('/api/data', methods=['GET'])
def data():
    return jsonify(service.dao.return_form_data())

