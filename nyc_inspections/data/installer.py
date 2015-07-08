#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "Ryan Kanno <ryankanno@localkinegrinds.com>"
__url__ = ""
__version__ = ""
__license__ = ""


import csv
from datetime import datetime
import itertools as IT
import logging
import os
import sys
import time
import traceback
import urllib


DATA_DIRECTORY = os.path.normpath(os.path.realpath(os.path.dirname(__file__)))

from ..models import Action
from ..models import Violation
from ..models import Cuisine
from ..models import Restaurant
from ..models import Inspection
from ..models import BOROUGHS
from ..database import db_session


DATA_URL = ("https://data.cityofnewyork.us/api/views/xx67-kt59/"
            "rows.csv?accessType=DOWNLOAD")

CSV_DATETIME_FORMAT = '%m/%d/%Y'


ACTION_CACHE = {}
CUISINE_CACHE = {}
VIOLATION_CACHE = {}
RESTAURANT_CACHE = {}
INSPECTION_CACHE = []


def process_data(data_file_path):
    logging.debug("Begin processing data file: {0}\n".format(data_file_path))

    with open(data_file_path, 'rb') as f:
        rdr = csv.DictReader(f, delimiter=',')
        rdr.next()

        process_metadata_into_cache(rdr)
        bulk_save_metadata_cache()

        f.seek(0)
        rdr.next()

        process_inspections_into_cache(rdr)
        bulk_save_inspections()

    logging.debug("End processing {0}\n".format(data_file_path))


def process_metadata_into_cache(reader):
    for idx, row in enumerate(reader):
        logging.debug("Processing row {0}".format(idx))
        _process_into_cache(row, process_inspections=False)


def process_inspections_into_cache(reader):
    for idx, row in enumerate(reader):
        logging.debug("Processing row {0}".format(idx))
        _process_into_cache(row, process_inspections=True)


def bulk_save_metadata_cache():
    violation_dict_list = [violation for violation in VIOLATION_CACHE.values()]
    violation_list = []
    for violation_dict in violation_dict_list:
        violation_list.append(violation_dict.values())

    db_session.bulk_save_objects(ACTION_CACHE.values(), return_defaults=True)
    db_session.bulk_save_objects(CUISINE_CACHE.values(), return_defaults=True)
    db_session.bulk_save_objects(
        list(IT.chain(*violation_list)),
        return_defaults=True)
    db_session.bulk_save_objects(
        RESTAURANT_CACHE.values(),
        return_defaults=True)
    db_session.commit()


def bulk_save_inspections():
    db_session.bulk_save_objects(INSPECTION_CACHE, return_defaults=False)
    db_session.commit()


def _process_into_cache(row, process_inspections=False):
    action = _process_action_row(row)
    cuisine = _process_cuisine_row(row)
    violation = _process_violation_row(row)
    restaurant = _process_restaurant_row(row)

    if process_inspections:
        _process_inspection_row(row, action, cuisine, violation, restaurant)


def _process_action_row(row):
    action_desc = row['ACTION'].strip()
    if action_desc not in ACTION_CACHE:
        action = Action(action_desc)
        ACTION_CACHE[action_desc] = action
    return ACTION_CACHE[action_desc]


def _process_cuisine_row(row):
    cuisine_name = row['CUISINE DESCRIPTION'].strip().decode('iso-8859-1')
    if cuisine_name not in CUISINE_CACHE:
        cuisine = Cuisine(cuisine_name)
        CUISINE_CACHE[cuisine_name] = cuisine
    return CUISINE_CACHE[cuisine_name]


def _process_violation_row(row):
    violation_code = row['VIOLATION CODE'].strip()
    violation_desc = row['VIOLATION DESCRIPTION'].strip().decode('iso-8859-1')
    if violation_code not in VIOLATION_CACHE:
        is_critical = row['CRITICAL FLAG'].strip() == 'Critical'
        violation = Violation(code=violation_code,
                              description=violation_desc,
                              is_critical=is_critical)
        VIOLATION_CACHE[violation_code] = {violation_desc: violation}
        return violation
    else:
        if violation_desc not in VIOLATION_CACHE[violation_code]:
            is_critical = row['CRITICAL FLAG'].strip() == 'Critical'
            violation = Violation(code=violation_code,
                                  description=violation_desc,
                                  is_critical=is_critical)
            VIOLATION_CACHE[violation_code][violation_desc] = violation
            return violation
        else:
            return VIOLATION_CACHE[violation_code][violation_desc]


def _process_restaurant_row(row):
    unique_id = row['CAMIS'].strip()

    if unique_id not in RESTAURANT_CACHE:
        name = row['DBA'].strip().decode('iso-8859-1')
        building = row['BUILDING'].strip()
        street = row['STREET'].strip()
        zip_code = row['ZIPCODE'].strip()
        borough = BOROUGHS.get(row['BORO'].strip().lower(), -1)
        phone = row['PHONE'].strip()
        restaurant = Restaurant(unique_id, name, building,
                                street, zip_code, borough, phone)
        RESTAURANT_CACHE[unique_id] = restaurant
    return RESTAURANT_CACHE[unique_id]


def _process_inspection_row(row, action, cuisine, violation, restaurant):
    if row['INSPECTION DATE'].strip():
        inspection_params = {}
        inspection_params['restaurant_id'] = restaurant.id
        inspection_params['cuisine_id'] = cuisine.id
        inspection_params['action_id'] = action.id
        inspection_params['violation_id'] = violation.id
        inspection_params['inspected_at'] = datetime.\
            strptime(row['INSPECTION DATE'].strip(), CSV_DATETIME_FORMAT)
        inspection_params['inspection_type'] = row['INSPECTION TYPE'].strip()
        inspection_params['score'] = row['SCORE'].strip()
        inspection_params['current_grade'] = row['GRADE'].strip()
        if row['GRADE DATE'].strip():
            inspection_params['graded_at'] = datetime.\
                strptime(row['GRADE DATE'].strip(), CSV_DATETIME_FORMAT)
        inspection_params['generated_at'] = datetime.\
            strptime(row['RECORD DATE'].strip().split(".")[0],
                     CSV_DATETIME_FORMAT)
        inspection = Inspection(**inspection_params)
        INSPECTION_CACHE.append(inspection)


def download_data_from_socrata(file_path=None):

    def download_progress(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write("\r Downloading " + DATA_URL + " to " +
                         inspection_data_file_path + ("... %d%%" % percent))
        sys.stdout.flush()

    inspection_data_filename = "nyc-inspection-data-{0}.sqlite".format(
        time.strftime("%Y%m%d-%H%M%S"))

    inspection_data_file_path = os.path.join('/tmp', inspection_data_filename) \
        if file_path is None else file_path

    urllib.urlretrieve(
        DATA_URL,
        inspection_data_file_path,
        reporthook=download_progress)

    return inspection_data_file_path


def cleanup():
    logging.debug("Cleaning up")


def seed_database(file_path):
    try:
        process_data(file_path)
    except KeyboardInterrupt:
        logging.error("OMGWTFBBQ: CTRL-C, ftl.")
        sys.exit(1)
    except Exception:
        trace = traceback.format_exc()
        logging.error("OMGWTFBBQ: {0}".format(trace))
        sys.exit(1)
    finally:
        cleanup()

    # Yayyy-yah
    return 0


# vim: filetype=python
