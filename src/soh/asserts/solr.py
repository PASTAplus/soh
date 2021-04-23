#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: solr

:Synopsis:

:Author:
    servilla

:Created:
    3/30/18
"""
from http import HTTPStatus

import aiohttp
import daiquiri

from soh.config import Config


logger = daiquiri.getLogger('solr.py: ' + __name__)


async def is_down(host=None):
    url = 'http://' + host + ':8983/solr/#/collection1/query'
    assert_is_down = True
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                 r = resp.status
        assert_is_down = r != HTTPStatus.OK
        if assert_is_down:
            msg = f"{__file__}: Status code is {r}"
            logger.warning(msg)
    except Exception as e:
        logger.error(e)
    return assert_is_down
