#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from nose.tools import ok_
from nyc_inspections.models import BOROUGHS
from nyc_inspections.models import Action
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


# vim: filetype=python
