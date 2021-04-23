#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: apache

:Synopsis:

:Author:
    servilla

:Created:
    3/31/18
"""
from http import HTTPStatus

import aiohttp
import daiquiri

from soh.config import Config


logger = daiquiri.getLogger('apache.py: ' + __name__)


async def is_down(host=None):
    url = 'http://' + host
    assert_is_down = True
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                 r = resp.status
        # Assert down only for server error and higher
        assert_is_down = r >= HTTPStatus.INTERNAL_SERVER_ERROR
        if assert_is_down:
            msg = f"{__file__}: Status code is {r}"
            logger.warning(msg)
    except Exception as e:
        logger.error(e)
    return assert_is_down
