#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nyc_inspections import app
from database import db_session
from extensions import cache
from flask import abort
from flask import jsonify
from flask import request
from models import Cuisine
from models import Inspection
from models import Restaurant


def _make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.values.items())))
    return (path + args).encode('utf-8')


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/restaurants/by_name", methods=['POST'])
@cache.cached(key_prefix=_make_cache_key)
def find_restaurants_by_name():
    results = []
    name = request.form.get('name', '', type=str).strip()

    if name:
        filterspec = Restaurant.name.like("%{0}%".format(name.upper()))
        restaurants = Restaurant.query.filter(filterspec)

        for restaurant in restaurants:
            results.append(restaurant.serialize)

    return jsonify(restaurants=results)


@app.route("/restaurants/by_cuisine", methods=['POST'])
@cache.cached(key_prefix=_make_cache_key)
def find_restaurants_by_cuisine():
    results = []
    cuisine = request.form.get('cuisine', '', type=str).strip()
    if cuisine:
        filterspec = Cuisine.name.like("%{0}%".format(cuisine.upper()))
        inspections = Inspection.query.\
            join(Cuisine).join(Restaurant).filter(filterspec)

        for inspection in inspections:
            results.append(inspection.restaurant.serialize)

    return jsonify(restaurants=results)


@app.route("/restaurants/<int:restaurant_id>", methods=['GET'])
@cache.cached(key_prefix=_make_cache_key)
def get_restaurant_by_id(restaurant_id):
    restaurant = {}
    if restaurant_id:
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            return jsonify(restaurant.serialize)
    return abort(404)


# vim: filetype=python
