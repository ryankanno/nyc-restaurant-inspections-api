#!/usr/bin/env python
# -*- coding: utf-8 -*-


def empty_dict(dict, keys=None):
    if keys:
        for key in keys:
            if key in dict:
                del dict[key]
    else:
        dict.clear()

# vim: filetype=python
