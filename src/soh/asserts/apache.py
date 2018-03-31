#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: apache

:Synopsis:

:Author:
    servilla

:Created:
    3/31/18
"""
import daiquiri
import requests

logger = daiquiri.getLogger('apache.py: ' + __name__)


def is_down(host=None):
    url = 'http://' + host + '/nis'
    assert_is_down = True
    try:
        r = requests.get(url=url, timeout=5.0)
        assert_is_down = r.status_code != requests.codes.ok
    except Exception as e:
        logger.error(e)
    return assert_is_down
