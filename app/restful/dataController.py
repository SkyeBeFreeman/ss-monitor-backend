#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import app
# from flask import Flask, jsonify, request, abort
# from datetime import datetime

@app.route('/api/data', methods=['GET'])
def getData():
	return "Hello World"
