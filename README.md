#ny-restaurant-inspections

A small Flask + Redis weekend-project that returns the latest and greatest restaurant inspections for NYC restaurants.

Data courtesy of https://nycopendata.socrata.com/Health/Restaurant-Inspection-Results/4vkw-7nck

##install

###data

To create the database as a temp SQL Lite database, run the following command:

`python data/install.py`

Note: At some point, this will just pull from the above url, but in the
meantime, bear with me. :D

###deploy

To run the flask app, make sure you have Flask installed:

`python api.py`
