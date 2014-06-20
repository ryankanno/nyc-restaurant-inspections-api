#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

from flask import Flask
from flask import request
from flask import jsonify
from database import db_session

PROJECT_ROOT = os.path.normpath(os.path.realpath(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from models import Restaurant

app = Flask(__name__)


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/", methods=['POST'])
def search():
    results = []
    name = request.form.get('name', '', type=str).strip()

    if name:
        filterspec = Restaurant.name.like("%{0}%".format(name.upper()))
        restaurants = Restaurant.query.filter(filterspec)

        for restaurant in restaurants:
            results.append(restaurant.serialize)

    return jsonify(restaurants=results)


if __name__ == "__main__":
    app.run(debug=True)


# vim: filetype=python
