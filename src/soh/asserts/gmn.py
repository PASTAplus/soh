#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: gmn

:Synopsis:

:Author:
    servilla

:Created:
    4/12/18
"""
import daiquiri
import requests

logger = daiquiri.getLogger('gmn.py: ' + __name__)


def is_down(host=None):
    url = 'https://' + host + '/mn/home'
    assert_is_down = True
    try:
        r = requests.get(url=url, allow_redirects=False, timeout=5.0)
        # Assert down only for server error and higher
        assert_is_down = r.status_code != requests.codes.ok
    except Exception as e:
        logger.error(e)
    return assert_is_down