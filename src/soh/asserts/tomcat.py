#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: tomcat

:Synopsis:

:Author:
    servilla

:Created:
    3/30/18
"""
import daiquiri
import requests

logger = daiquiri.getLogger('tomcat.py: ' + __name__)


def is_down(host=None):
    url = 'http://' + host + ':8080'
    assert_is_down = True
    try:
        r = requests.get(url=url, timeout=5.0)
        assert_is_down = r.status_code != requests.codes.ok
    except Exception as e:
        logger.error(e)
    return assert_is_down
