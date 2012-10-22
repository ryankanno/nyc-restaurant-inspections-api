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


# TODO : Add address search
@app.route("/", methods=['POST'])
def search():
    results = []
    name = request.form.get('name', '', type=str).strip()
    filterspec = Restaurant.name.like("%{0}%".format(name.upper()))
    restaurants = Restaurant.query.filter(filterspec)

    for restaurant in restaurants:
        i = []
        for inspection in restaurant.inspections:
            inspect = {
                'current_grade': inspection.current_grade,
                'inspected_date': inspection.graded_at.
                strftime('%Y-%m-%dT%H:%M:%S'),
                'score': inspection.score,
            }

            if inspection.action:
                inspect['action_code'] = inspection.action.code
                inspect['action_desc'] = inspection.action.description

            if inspection.violation:
                inspect['violation_code'] = inspection.violation.code
                inspect['violation_desc'] = inspection.violation.description

            i.append(inspect)

        i.sort(key=lambda x: x['inspected_date'], reverse=True)
        r = restaurant.serialize
        r['inspections'] = i
        results.append(r)

    return jsonify(data=results)


if __name__ == "__main__":
    app.run(debug=True)


# vim: filetype=python
