#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import ok_
from nyc_inspections.utilities import empty_dict
import unittest


class TestUtilities(unittest.TestCase):

    def test_empty_dict(self):
        d1 = {"foo": 1}
        ok_(len(d1) == 1)
        empty_dict(d1)
        ok_(len(d1) == 0)
        d2 = {"foo": 1, "bar": 2}
        ok_(len(d2) == 2)
        ok_(d2["foo"] == 1)
        empty_dict(d2, ["foo"])
        ok_("foo" not in d2)
        ok_("bar" in d2)


# vim: filetype=python
