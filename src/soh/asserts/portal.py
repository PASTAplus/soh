#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: portal

:Synopsis:

:Author:
    servilla

:Created:
    4/12/18
"""
import daiquiri
import requests

from soh.config import Config


logger = daiquiri.getLogger('portal.py: ' + __name__)


def is_down(host=None):
    url = 'https://' + host + '/nis/'
    assert_is_down = True
    try:
        r = requests.get(url=url, allow_redirects=False, timeout=Config.TIMEOUT)
        # Assert down only for server error and higher
        assert_is_down = r.status_code != requests.codes.ok
        if assert_is_down:
            msg = f"{__file__}: Status code is {r.status_code}"
            logger.warning(msg)
    except Exception as e:
        logger.error(e)
    return assert_is_down