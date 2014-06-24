#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import locale
import os

from flask import Flask
from flask import request
from flask import jsonify
from flask.ext.cache import Cache
from database import db_session

PROJECT_ROOT = os.path.normpath(os.path.realpath(os.path.dirname(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from models import Restaurant

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})


def _make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.values.items())))
    return (path + args).encode('utf-8')


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/", methods=['POST'])
@cache.cached(key_prefix=_make_cache_key)
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
