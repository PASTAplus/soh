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

from soh.config import Config


logger = daiquiri.getLogger('apache.py: ' + __name__)


def is_down(host=None):
    url = 'http://' + host
    assert_is_down = True
    try:
        r = requests.get(url=url, allow_redirects=False, timeout=Config.TIMEOUT)
        # Assert down only for server error and higher
        assert_is_down = r.status_code >= requests.codes.server_error
        if assert_is_down:
            msg = f"{__file__}: Status code is {r.status_code}"
            logger.warning(msg)
    except Exception as e:
        logger.error(e)
    return assert_is_down
