
.. image:: https://travis-ci.org/ryankanno/nyc-restaurant-inspections-api.svg?branch=master
   :target: https://travis-ci.org/ryankanno/nyc-restaurant-inspections-api

.. image:: https://coveralls.io/repos/ryankanno/nyc-restaurant-inspections-api/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/ryankanno/nyc-restaurant-inspections-api?branch=master

API for NYC restaurant inspections
==================================

A Flask + Redis weekend project that returns NYC restaurant inspection data.

Data courtesy of https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/xx67-kt59

Install
=======

* Install redis-server (sudo port install redis-server, brew install redis)
* Install the requirements by running `pip install -r requirements.txt`

Download the Socrata data
-------------------------

To download the socrata, run the following command:

.. code:: python

  python manage.py download_data

Make sure to remember the output file path (or pass in a path of your own)

.. code:: python

  python manage.py download_data --help

Create the database
-------------------

To create the database, run the following command:

.. code:: python

  python manage.py create_db

Seed the database
-----------------

To seed the database, run the following command:

.. code:: python

  python manage.py seed_db -f <output_file_path_from_download_data_command>

Run Server
----------

To run the server, run the following command:

.. code:: python

  python manage.py runserver

Drop the database
-----------------

After you're done playing with this magical goodness,
to drop the database, run the following command:

.. code:: python

  python manage.py drop_db


Examples
========

Here are some curl commands to play around with the api:

**Finding all restaurants (and inspections) with Japanese in their name**

.. code::

  curl -s -H "Accept:  application/json" -d "name=Japanese" http://localhost:5000/restaurants/by_name | python -mjson.tool


**Finding all restaurants (and inspections) with Japanese cuisine**

.. code::

  curl -s -H "Accept:  application/json" -d "cuisine=Japanese" http://localhost:5000/restaurants/by_cuisine | python -mjson.tool

**Finding restaurant with id 10**

.. code::

  curl -s -H "Accept:  application/json" http://localhost:5000/restaurants/10 | python -mjson.tool

TODO
====

License
=======
MIT
