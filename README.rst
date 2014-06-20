nyc-inspections
===============

.. image:: https://travis-ci.org/ryankanno/nyc-inspections.png?branch=master
   :target: https://travis-ci.org/ryankanno/nyc-inspections

.. image:: https://coveralls.io/repos/ryankanno/nyc-inspections/badge.png
   :target: https://coveralls.io/r/ryankanno/nyc-inspections

API for NYC restaurant inspections.

A tiny Flask + Redis weekend project that returns NYC restaurant inspections.

Data courtesy of https://nycopendata.socrata.com/Health/Restaurant-Inspection-Results/4vkw-7nck

install
-------

data
~~~~

To create the database as a temp SQLite database, run the following command:

`python nyc_inspections/data/install.py`

Note: At some point, this will pull data from the above url, but in the
meantime, bear with me. :D

deploy
~~~~~~

To run the flask app, make sure you have Flask installed:

`python nyc_inspections/api.py`


test
~~~~

Here are some curl commands to play around with the api:

**Finding all restaurants with Japanese in their name**

`curl -s -H "Accept:  application/json" -d "name=Japanese" http://localhost:5000 | python -mjson.tool`

todo
----

license
-------
MIT
