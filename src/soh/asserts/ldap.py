#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: ldap

:Synopsis:

:Author:
    servilla

:Created:
    3/30/18
"""
import daiquiri
from ldap3 import Server, Connection, ALL

from soh.config import Config


logger = daiquiri.getLogger('ldap.py: ' + __name__)


async def is_down(host=None):
    server = Server(host, use_ssl=True, get_info=ALL)
    assert_is_down = True
    try:
        conn = Connection(server, auto_bind=True, receive_timeout=15)
        if conn.result['result'] == Config.UP:
            assert_is_down = False
    except Exception as e:
        logger.error(e)
    return assert_is_down
