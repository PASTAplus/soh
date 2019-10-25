#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: auth.py

:Synopsis:

:Author:
    servilla

:Created:
    10/25/19
"""
import daiquiri
import requests

logger = daiquiri.getLogger('auth.py: ' + __name__)

def is_down(host=None):
    url = 'https://' + host + '/auth/accept'
    assert_is_down = True
    try:
        r = requests.get(url=url, allow_redirects=False, timeout=5.0)
        # Assert down only for server error and higher
        assert_is_down = r.status_code != requests.codes.bad
    except Exception as e:
        logger.error(e)
    return assert_is_down