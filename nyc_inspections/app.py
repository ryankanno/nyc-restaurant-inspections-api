#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import DefaultConfig
from database import init_engine

from flask import Flask

from extensions import cache

import json
import logging
import logging.config
import os


def get_app(config=None, **kwargs):
    """Creates a Flask application"""
    app = Flask(__name__, **kwargs)

    configure_app(app, config)

    init_engine(app.config['DATABASE_URI'])

    cache.init_app(app)

    configure_logging(app)

    return app


def configure_app(app, config):
    app.config.from_object(DefaultConfig)

    if config is not None:
        app.config_from_object(config)

    if 'CONFIG_ENVVAR' in app.config:
        app.config.from_envvar(app.config['CONFIG_ENVVAR'])

    if 'TEMPLATE_DIR' in app.config:
        app.template_folder = app.config['TEMPLATE_DIR']

    if 'STATIC_DIR' in app.config:
        app.static_folder = app.config['STATIC_DIR']


def configure_logging(app):
    log_ini = os.path.join(app.root_path, app.config['LOG_INI'])

    if os.path.exists(log_ini):
        with open(log_ini, 'rt') as f:
            log_config = json.load(f)
        logging.config.dictConfig(log_config)

# vim: filetype=python
