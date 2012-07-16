from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
import csv
import logging
from datetime import datetime
import codecs

import sys, os
DATA_DIRECTORY = os.path.normpath(os.path.realpath(os.path.dirname(__file__)))

sys.path.insert(0, os.path.join(DATA_DIRECTORY, os.path.pardir))

from models import Action, Violation, Cuisine, Restaurant, Inspection
from database import db_session

import codecs


def load_action_data(truncate=False):

    with open(os.path.join(DATA_DIRECTORY, 'Action.txt'), 'rb') as f:
        reader = csv.DictReader(f, delimiter=',')
        header_row = reader.next()

        for row in reader:
            start_at = datetime.strptime(row['STARTDATE'].strip(), '%Y-%m-%d %H:%M:%S')
            end_at = datetime.strptime(row['ENDDATE'].strip(), '%Y-%m-%d %H:%M:%S')

            action = Action(row['ACTIONCODE'].strip(), 
                            row['ACTIONDESC'].strip(),
                            start_at, end_at)
            db_session.add(action)
            db_session.commit()


def load_violation_data(truncate=False):

    with open(os.path.join(DATA_DIRECTORY, 'Violation.txt'), 'rb') as f:
        reader = csv.DictReader(f, delimiter=',')
        header_row = reader.next()

        for row in reader:
            start_at = datetime.strptime(row['STARTDATE'], '%Y-%m-%d %H:%M:%S')
            end_at = datetime.strptime(row['ENDDATE'], '%Y-%m-%d %H:%M:%S')
            is_critical = True if row['CRITICALFLAG'] == "Y" else False

            violation = Violation(row['VIOLATIONCODE'].strip(), 
                                  row['VIOLATIONDESC'].strip().decode('iso-8859-1'),
                                  is_critical, start_at, end_at)
            db_session.add(violation)
            db_session.commit()


def load_cuisine_data(truncate=False):

    with open(os.path.join(DATA_DIRECTORY, 'Cuisine.txt'), 'rb') as f:
        reader = csv.DictReader(f, delimiter=',')
        header_row = reader.next()

        for row in reader:
            cuisine = Cuisine(row['CUISINECODE'].strip(),
                              row['CODEDESC'].strip().decode('iso-8859-1'))
            db_session.add(cuisine)
            db_session.commit()


def load_inspection_data(truncate=False):

    with open(os.path.join(DATA_DIRECTORY, 'WebExtract.txt'), 'rb') as f:
        reader = csv.DictReader(f, delimiter=',')
        header_row = reader.next()

        i = 1
        for row in reader:
            print "Parsing line " + str(i)
            i += 1

            # Skip anything with an empty grade date
            if row['GRADEDATE'].strip():
                unique_id = row['CAMIS']
                restaurant = Restaurant.query.filter_by(unique_id=unique_id).first()
                if restaurant is None:
                    name = row['DBA'].strip().decode('iso-8859-1')
                    borough = int(row['BORO'].strip())
                    building = row['BUILDING'].strip()
                    street = row['STREET'].strip()
                    zipcode = row['ZIPCODE'].strip()
                    phone = row['PHONE'].strip()
                    restaurant = Restaurant(unique_id, name, building, street,
                            zipcode, phone)
                    db_session.add(restaurant)
                    db_session.commit()

                inspection_params = {'restaurant_id': restaurant.id}

                cuisine = Cuisine.query.filter_by(code=row['CUISINECODE'].strip()).first()
                if cuisine is not None:
                    inspection_params['cuisine_id'] = cuisine.id

                inspection_params['inspected_at'] = datetime.strptime(row['INSPDATE'].strip(), '%Y-%m-%d %H:%M:%S')

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
                inspection_params['graded_at'] = datetime.strptime(row['GRADEDATE'].strip(), '%Y-%m-%d %H:%M:%S')
                inspection_params['generated_at'] = datetime.strptime(row['RECORDDATE'].strip().split(".")[0], '%Y-%m-%d %H:%M:%S')

                inspection = Inspection(**inspection_params)
                db_session.add(inspection)
                db_session.commit()


if __name__ == "__main__":
    from database import init_db

    init_db()
    load_action_data()
    load_violation_data()
    load_cuisine_data()
    load_inspection_data()
