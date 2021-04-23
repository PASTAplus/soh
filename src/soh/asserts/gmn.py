#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: gmn

:Synopsis:

:Author:
    servilla

:Created:
    4/12/18
"""
from http import HTTPStatus

import aiohttp
import daiquiri

from soh.config import Config


logger = daiquiri.getLogger('gmn.py: ' + __name__)


async def is_down(host=None):
    url = 'https://' + host + '/mn/v2/node'
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