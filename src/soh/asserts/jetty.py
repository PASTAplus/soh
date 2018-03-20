#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: jetty

:Synopsis:

:Author:
    servilla

:Created:
    3/16/18
"""
import daiquiri
import requests

logger = daiquiri.getLogger('jetty.py: ' + __name__)


def is_down(host=None):
    url = 'http://' + host + ':8080'
    is_down = True
    try:
        r = requests.get(url=url)
        is_down = r.status_code != requests.codes.ok
    except Exception as e:
        logger.error(e)
    return is_down
