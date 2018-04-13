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
    url = 'http://' + host
    assert_is_down = True
    try:
        r = requests.get(url=url, allow_redirects=False, timeout=5.0)
        # Assert down only for server error and higher
        assert_is_down = r.status_code >= requests.codes.server_error
    except Exception as e:
        logger.error(e)
    return assert_is_down
