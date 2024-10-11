#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: auth.py

:Synopsis:

:Author:
    servilla

:Created:
    10/25/19
"""
from http import HTTPStatus

import aiohttp
import daiquiri

from soh.config import Config


logger = daiquiri.getLogger('auth.py: ' + __name__)


async def is_down(host=None):
    # Temporary patch for changes between auth and auth-d URL pattern
    if host == "auth.edirepository.org":
        url = 'https://' + host + '/auth/ping'
    else:
        url = 'https://' + host + '/auth/v1/ping'
    assert_is_down = True
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                 r = resp.status
        # Assert down for any response other than bad request
        assert_is_down = r != HTTPStatus.OK
        if assert_is_down:
            msg = f"{__file__}: Status code is {r}"
            logger.warning(msg)
    except Exception as e:
        logger.error(e)
    return assert_is_down