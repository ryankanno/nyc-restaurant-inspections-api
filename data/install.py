from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
import csv
import logging

import sys, os
DATA_DIRECTORY = os.path.normpath(os.path.realpath(os.path.dirname(__file__)))

sys.path.insert(0, os.path.join(DATA_DIRECTORY, os.path.pardir))

from models import Action
from database import db_session


def load_action_data(truncate=False):

    with open(os.path.join(DATA_DIRECTORY, 'Action.txt'), 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        header_row = reader.next()

        for row in reader:
            action = Action(row['ACTIONCODE'].strip(), 
                            row['ACTIONDESC'].strip())
            db_session.add(action)
            db_session.commit()

if __name__ == "__main__":
    from database import init_db

    init_db()
    load_action_data()
