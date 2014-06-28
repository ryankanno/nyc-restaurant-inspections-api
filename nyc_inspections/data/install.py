#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = ['main']
__author__ = "Ryan Kanno <ryankanno@localkinegrinds.com>"
__url__ = ""
__version__ = ""
__license__ = ""


import logging
import sys
import os
import csv

from datetime import datetime
from zipfile import ZipFile

DATA_DIRECTORY = os.path.normpath(os.path.realpath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(DATA_DIRECTORY, os.path.pardir))

from models import Action
from models import Violation
from models import Cuisine
from models import Restaurant
from models import Inspection
from ..database import db_session
from ..database import init_db


LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'


DATA_ZIP_FILE = 'dohmh_restaurant-inspections_002.zip'
CSV_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def load_file_and_process(path, process_func):
    logging.debug("Begin processing {0}\n".format(path))

    with open(path, 'rb') as f:
        rdr = csv.DictReader(f, delimiter=',')
        rdr.next()

        i = 0
        for row in rdr:
            i += 1
            logging.debug("Processing row {0} from {1}".format(i, path))
            process_func(row)

    logging.debug("End processing {0}\n".format(path))


def _get_start_end_date_tuple(row):
    return datetime.strptime(row['STARTDATE'].strip(), CSV_DATETIME_FORMAT), \
        datetime.strptime(row['ENDDATE'].strip(), CSV_DATETIME_FORMAT)


def _process_action_row(row):
    start, end = _get_start_end_date_tuple(row)

    action = Action(row['ACTIONCODE'].strip(),
                    row['ACTIONDESC'].strip(), start, end)

    db_session.add(action)
    db_session.commit()


def _process_violation_row(row):
    start, end = _get_start_end_date_tuple(row)
    is_critical = True if row['CRITICALFLAG'] == "Y" else False

    violation = Violation(row['VIOLATIONCODE'].strip(),
                          row['VIOLATIONDESC'].strip().decode('iso-8859-1'),
                          is_critical, start, end)

    db_session.add(violation)
    db_session.commit()


def _process_cuisine_row(row):
    cuisine = Cuisine(row['CUISINECODE'].strip(),
                      row['CODEDESC'].strip().decode('iso-8859-1'))

    db_session.add(cuisine)
    db_session.commit()


def _process_and_return_restaurant(row):
    unique_id = row['CAMIS'].strip()
    name = row['DBA'].strip().decode('iso-8859-1')
    building = row['BUILDING'].strip()
    street = row['STREET'].strip()
    zipcode = row['ZIPCODE'].strip()
    borough = int(row['BORO'].strip())
    phone = row['PHONE'].strip()
    restaurant = Restaurant(unique_id, name, building,
                            street, zipcode, borough, phone)

    db_session.add(restaurant)
    db_session.commit()

    return restaurant


def _process_inspection_row(row):
    if row['GRADEDATE'].strip():
        restaurant = Restaurant.query.\
            filter_by(unique_id=row['CAMIS'].strip()).first()

        if restaurant is None:
            restaurant = _process_and_return_restaurant(row)

        inspection_params = {'restaurant_id': restaurant.id}

        cuisine = Cuisine.query.\
            filter_by(code=row['CUISINECODE'].strip()).first()

        if cuisine is not None:
            inspection_params['cuisine_id'] = cuisine.id

        inspection_params['inspected_at'] = datetime.\
            strptime(row['INSPDATE'].strip(), CSV_DATETIME_FORMAT)

        action = Action.query.filter_by(code=row['CUISINECODE'].strip()).\
            filter(Action.end_at >= inspection_params['inspected_at']).\
            filter(inspection_params['inspected_at'] >= Action.start_at).\
            first()

        if action is not None:
            inspection_params['action_id'] = action.id

        violation = Violation.query.filter_by(code=row['VIOLCODE'].strip()).\
            filter(Violation.end_at >= inspection_params['inspected_at']).\
            filter(inspection_params['inspected_at'] >= Violation.start_at).\
            first()

        if violation is not None:
            inspection_params['violation_id'] = violation.id

        inspection_params['score'] = row['SCORE'].strip()
        inspection_params['current_grade'] = row['CURRENTGRADE'].strip()
        inspection_params['graded_at'] = datetime.\
            strptime(row['GRADEDATE'].strip(), CSV_DATETIME_FORMAT)
        inspection_params['generated_at'] = datetime.\
            strptime(row['RECORDDATE'].strip().split(".")[0],
                     CSV_DATETIME_FORMAT)

        inspection = Inspection(**inspection_params)

        db_session.add(inspection)
        db_session.commit()


def init_workspace():
    logging.debug("Unzipping data file")

    zip = ZipFile(os.path.join(DATA_DIRECTORY, DATA_ZIP_FILE))
    zip.extractall(path=DATA_DIRECTORY)

    if (os.path.exists('/tmp/test.db')):
        logging.debug("Removing previous database")
        os.remove('/tmp/test.db')


def cleanup():
    logging.debug("Cleaning up")
    [os.remove(os.path.join(DATA_DIRECTORY, f))
        for f in os.listdir(DATA_DIRECTORY)
        if f.endswith(".txt") or f.endswith(".xls")]


def main(argv=None):
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

    init_workspace()
    init_db()

    file_processor_tuples = [
        ('Action.txt', _process_action_row),
        ('Violation.txt', _process_violation_row),
        ('Cuisine.txt', _process_cuisine_row),
        ('WebExtract.txt', _process_inspection_row)
    ]

    try:
        for fp in file_processor_tuples:
            load_file_and_process(os.path.join(DATA_DIRECTORY, fp[0]), fp[1])
    except KeyboardInterrupt as e:
        logging.error("OMGWTFBBQ: CTRL-C, ftl.")
        sys.exit(1)
    except Exception as e:
        logging.error("OMGWTFBBQ: {0}".format(e.args))
        sys.exit(1)
    finally:
        cleanup()

    # Yayyy-yah
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


# vim: filetype=python
