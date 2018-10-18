#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app, db, user_list, service
# from flask import Flask, jsonify, request, abort
# from datetime import datetime


@app.route('/api/start_watching', methods=['GET'])
def start_watching():
    service.monitor.start_watching(user_list)
    return "start_watching"


@app.route('/api/check_watching', methods=['GET'])
def check_watching():
    service.monitor.check_watching(user_list)
    return "check_watching"


@app.route('/api/stop_watching', methods=['GET'])
def stop_watching():
    service.monitor.stop_watching(user_list)
    return "stop_watching"

