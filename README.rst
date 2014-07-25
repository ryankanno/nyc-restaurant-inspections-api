nyc-inspections
===============

.. image:: https://travis-ci.org/ryankanno/nyc-inspections.png?branch=master
   :target: https://travis-ci.org/ryankanno/nyc-inspections

.. image:: https://coveralls.io/repos/ryankanno/nyc-inspections/badge.png
   :target: https://coveralls.io/r/ryankanno/nyc-inspections

API for NYC restaurant inspections.

A Flask + Redis weekend project that returns NYC restaurant inspection data.

Data courtesy of https://nycopendata.socrata.com/Health/Restaurant-Inspection-Results/4vkw-7nck

install
-------

data
~~~~

To create the database as a temp SQLite database, run the following command:

`python -m nyc_inspections.data.install`

Note: At some point, this will pull data from the above url, but in the
meantime, bear with me. :D

deploy
~~~~~~

To run the flask app, make sure you have Flask installed:

`python -m nyc_inspections.api`


test
~~~~

Here are some curl commands to play around with the api:

**Finding all restaurants with Japanese in their name**

`curl -s -H "Accept:  application/json" -d "name=Japanese" http://localhost:5000/find/by_name | python -mjson.tool`

**Finding restaurant with id 10**

`curl -s -H "Accept:  application/json" http://localhost:5000/restaurants/10 | python -mjson.tool`

todo
----

license
-------
MIT
