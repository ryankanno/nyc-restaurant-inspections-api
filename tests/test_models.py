#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
from nyc_inspections.models import BOROUGHS
import unittest


class TestModels(unittest.TestCase):

    def test_boroughs(self):
        ok_(BOROUGHS[1] == 'Manhattan')
        ok_(BOROUGHS[2] == 'The Bronx')
        ok_(BOROUGHS[3] == 'Brooklyn')
        ok_(BOROUGHS[4] == 'Queens')
        ok_(BOROUGHS[5] == 'Staten Island')
        ok_(len(BOROUGHS) == 5)


# vim: filetype=python
