#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
]

here = os.path.dirname(os.path.realpath(__file__))

# Metadata

meta = {}
re_meta = re.compile(r'__(\w+?)__\s*=\s*(.*)')
re_version = re.compile(r'VERSION\s*=.*?\((.*?)\)')
strip_quotes = lambda s: s.strip("\"'")


def add_version(match):
    return {'VERSION': match.group(1).replace(" ", "").replace(",", ".")}


def add_meta(match):
    attr_name, attr_value = m.groups()
    return {attr_name: strip_quotes(attr_value)}


patterns = {
    re_meta: add_meta,
    re_version: add_version
}


with open(os.path.join(here, 'nyc_inspections/__init__.py'), 'r') as f:
    for line in f:
        for pattern, handler in patterns.items():
            m = pattern.match(line.strip())
            if m:
                meta.update(handler(m))

# Requires

requires = ['Flask==0.10.1',
            'SQLAlchemy==1.0.6',
            'Flask-SQLAlchemy==2.0',
            'Flask-Script>=2.0.5',
            'ordereddict',
            'Flask-Cache',
            'redis']

tests_require = ['flake8', 'mock', 'nose', 'nosexcover']

with open(os.path.join(here, 'README.rst')) as f:
    readme = f.read()

with open(os.path.join(here, 'CHANGES')) as f:
    changes = f.read()

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'License :: OSI Approved :: MIT License',
    'Topic :: Utilities'
]

setup(
    name='nyc-inspections',
    version=meta['VERSION'],
    description='API for NYC restaurant inspections',
    long_description=readme + '\n\n' + changes,
    author=meta['author'],
    author_email=meta['email'],
    url="https://github.com/ryankanno/nyc-inspections",
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'nyc_inspections': 'nyc_inspections'},
    install_requires=requires,
    license=meta['license'],
    tests_require=tests_require,
    classifiers=classifiers,
    test_suite='nose.collector'
)


# vim: filetype=python
