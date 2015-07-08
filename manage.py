#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from flask.ext.script import prompt_bool
from nyc_inspections import app
from nyc_inspections.extensions import cache
from nyc_inspections.data.installer import seed_database
from nyc_inspections.data.installer import download_data_from_socrata
from nyc_inspections.database import create_db as c_db
from nyc_inspections.database import drop_db as d_db
import sys


manager = Manager(app)


@manager.option('-f', '--file_path', dest='file_path')
def download_data(file_path):
    """
    Downloads NYC restaurant inspection data from Socrata to `file_path`
    """
    download_path = download_data_from_socrata(file_path)
    sys.stdout.write("\r\nDownloaded Socrata data to {0}\n".
                     format(download_path))


@manager.command
def create_db():
    """
    Creates database
    """
    c_db(app.config['DATABASE_URI'])


@manager.command
def drop_db():
    """
    Drops database
    """
    if prompt_bool("Are you sure you want to remove all your data"):
        d_db(app.config['DATABASE_URI'])


@manager.option('-f', '--file_path', dest='file_path', required=True)
def seed_db(file_path):
    """
    Downloads data from socrata to `file_path` and seeds data
    """
    seed_database(file_path)


@manager.command
def flush_cache():
    """
    Flush cache
    """
    with app.app_context():
        cache.clear()

if __name__ == "__main__":
    manager.run()

# vim: filetype=python
