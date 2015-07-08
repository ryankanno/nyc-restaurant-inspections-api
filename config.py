#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class DefaultConfig(object):
    DEBUG = True

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_NAME = "nyc-restaurant-inspections"
    SECRET_KEY = "PLEASE_CHANGE_ME"

    DATABASE_URI = 'sqlite:////tmp/test.db'
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    STATIC_DIR = os.path.join(PROJECT_ROOT, 'nyc_inspections', 'apps', 'static')
    TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'nyc_inspections', 'apps', 'templates')

    LOG_INI = 'etc/logging.ini.json'

# vim: filetype=python
