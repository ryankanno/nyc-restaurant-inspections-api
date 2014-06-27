#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from nose.tools import ok_
from nyc_inspections.models import BOROUGHS
from nyc_inspections.models import Action
from nyc_inspections.models import Violation
import unittest


class TestModels(unittest.TestCase):

    def test_boroughs(self):
        ok_(BOROUGHS[1] == 'Manhattan')
        ok_(BOROUGHS[2] == 'The Bronx')
        ok_(BOROUGHS[3] == 'Brooklyn')
        ok_(BOROUGHS[4] == 'Queens')
        ok_(BOROUGHS[5] == 'Staten Island')
        ok_(len(BOROUGHS) == 5)

    def test_action(self):
        action_code = "10E"
        action_desc = "Something bad"
        action_start = datetime.datetime.utcnow()
        action_end = datetime.datetime.utcnow()
        action_params = {
            'code': action_code,
            'description': action_desc,
            'start_at': action_start,
            'end_at': action_end
        }
        action = Action(**action_params)
        ok_(action.code == action_code)
        ok_(action.description == action_desc)
        ok_(action.start_at == action_start)
        ok_(action.end_at == action_end)

    def test_violation(self):
        violation_code = "10E"
        violation_desc = "Bad violation"
        violation_is_critical = False
        violation_start = datetime.datetime.utcnow()
        violation_end = datetime.datetime.utcnow()
        violation_params = {
            'code': violation_code,
            'description': violation_desc,
            'start_at': violation_start,
            'end_at': violation_end
        }
        violation = Violation(**violation_params)
        ok_(violation.code == violation_code)
        ok_(violation.description == violation_desc)
        ok_(violation.is_critical == violation_is_critical)
        ok_(violation.start_at == violation_start)
        ok_(violation.end_at == violation_end)


# vim: filetype=python
