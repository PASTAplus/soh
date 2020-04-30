#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: solr

:Synopsis:

:Author:
    servilla

:Created:
    3/30/18
"""
import daiquiri
import requests

logger = daiquiri.getLogger('solr.py: ' + __name__)


def is_down(host=None):
    url = 'http://' + host + ':8983/solr/#/collection1/query'
    assert_is_down = True
    try:
        r = requests.get(url=url, allow_redirects=False, timeout=5.0)
        assert_is_down = r.status_code != requests.codes.ok
        if assert_is_down:
            msg = f"{__file__}: Status code is {r.status_code}"
            logger.warning(msg)
    except Exception as e:
        logger.error(e)
    return assert_is_down
