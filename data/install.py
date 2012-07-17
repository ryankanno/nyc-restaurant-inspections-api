from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
import csv
import logging
from datetime import datetime
import codecs

import sys, os
DATA_DIRECTORY = os.path.normpath(os.path.realpath(os.path.dirname(__file__)))

sys.path.insert(0, os.path.join(DATA_DIRECTORY, os.path.pardir))

from models import Action, Violation, Cuisine, Restaurant, Inspection
from database import db_session, init_db
from zipfile import ZipFile


DATA_ZIP_FILE = 'dohmh_restaurant-inspections_002.zip'
CSV_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def load_file_and_process(path, process_func):
    logging.debug("Begin processing {0}".format(path))

    with open(path, 'rb') as f:
        reader = csv.DictReader(f, delimiter=',')
        header_row = reader.next()
        i = 0
        for row in reader:
            i += 1
            logging.debug("Processing row {0} from {1}".format(i, path))
            process_func(row)

    logging.debug("End processing {0}\n".format(path))


def _get_start_end_date_tuple(row):
    return datetime.strptime(row['STARTDATE'].strip(), CSV_DATETIME_FORMAT), \
        datetime.strptime(row['ENDDATE'].strip(), CSV_DATETIME_FORMAT)


def _process_action_row(row):
    start, end = _get_start_end_date_tuple(row)

    action = Action(row['ACTIONCODE'].strip(), row['ACTIONDESC'].strip(), start, end)

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
    cuisine = Cuisine(row['CUISINECODE'].strip(), row['CODEDESC'].strip().decode('iso-8859-1'))

    db_session.add(cuisine)
    db_session.commit()


def _process_and_return_restaurant(row):
    unique_id=row['CAMIS'].strip()
    name = row['DBA'].strip().decode('iso-8859-1')
    building = row['BUILDING'].strip()
    street = row['STREET'].strip()
    zipcode = row['ZIPCODE'].strip()
    borough = int(row['BORO'].strip())
    phone = row['PHONE'].strip()
    restaurant = Restaurant(unique_id, name, building, street, zipcode, borough, phone)

    db_session.add(restaurant)
    db_session.commit()

    return restaurant


def _process_inspection_row(row):
    if row['GRADEDATE'].strip():
        restaurant = Restaurant.query.filter_by(unique_id=row['CAMIS'].strip()).first()
        if restaurant is None:
            restaurant = _process_and_return_restaurant(row)

        inspection_params = {'restaurant_id': restaurant.id }

        cuisine = Cuisine.query.filter_by(code=row['CUISINECODE'].strip()).first()
        if cuisine is not None:
            inspection_params['cuisine_id'] = cuisine.id

        inspection_params['inspected_at'] = datetime.strptime(row['INSPDATE'].strip(), CSV_DATETIME_FORMAT)

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
        inspection_params['graded_at'] = datetime.strptime(row['GRADEDATE'].strip(), CSV_DATETIME_FORMAT)
        inspection_params['generated_at'] = datetime.strptime(row['RECORDDATE'].strip().split(".")[0], CSV_DATETIME_FORMAT)

        inspection = Inspection(**inspection_params)

        db_session.add(inspection)
        db_session.commit()


def init_workspace():
    logging.debug("Unzipping data file")

    zip = ZipFile(os.path.join(DATA_DIRECTORY, DATA_ZIP_FILE))
    zip.extractall()

    if (os.path.exists('/tmp/test.db')):
        logging.debug("Removing previous database")
        os.remove('/tmp/test.db')
    

def cleanup():
    logging.debug("Cleaning up")
    [os.remove(f) for f in os.listdir(DATA_DIRECTORY) \
        if f.endswith(".txt") or f.endswith(".xls")] 


if __name__ == "__main__":

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
    except Exception, err:
        logging.error(err)
        cleanup()
