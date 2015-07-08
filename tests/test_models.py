#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
from nyc_inspections.models import BOROUGHS
from nyc_inspections.models import Action
from nyc_inspections.models import Cuisine
from nyc_inspections.models import Violation
import unittest


class TestModels(unittest.TestCase):

    def test_boroughs(self):
        ok_(BOROUGHS['manhattan'] == 1)
        ok_(BOROUGHS['bronx'] == 2)
        ok_(BOROUGHS['brooklyn'] == 3)
        ok_(BOROUGHS['queens'] == 4)
        ok_(BOROUGHS['staten island'] == 5)
        ok_(len(BOROUGHS) == 5)

    def test_action(self):
        action_desc = "Something bad"
        action_params = {
            'description': action_desc,
        }
        action = Action(**action_params)
        ok_(action.description == action_desc)

    def test_cuisine(self):
        cuisine_name = "Japanese"
        cuisine_params = {
            'name': cuisine_name,
        }
        cuisine = Cuisine(**cuisine_params)
        ok_(cuisine.name == cuisine_name)

    def test_violation(self):
        violation_code = "10E"
        violation_desc = "Bad violation"
        violation_is_critical = False
        violation_params = {
            'code': violation_code,
            'description': violation_desc,
        }
        violation = Violation(**violation_params)
        ok_(violation.code == violation_code)
        ok_(violation.description == violation_desc)
        ok_(violation.is_critical == violation_is_critical)


# vim: filetype=python
