#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: server

:Synopsis:

:Author:
    servilla

:Created:
    3/16/18
"""

import logging

import daiquiri

from soh.config import Config
from soh.asserts import server
from soh.asserts import jetty

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('server.py: ' + __name__)


class Server(object):

    @staticmethod
    def check_server(host=None):
        status = Config.UP
        if Server.server_is_down(host=host):
            status = status | Config.SERVER_DOWN
        return status

    @staticmethod
    def server_is_down(host=None):
        server_is_down = False
        server_uptime = server.uptime(host=host, user=Config.USER,
                                      key_path=Config.KEY_PATH,
                                      key_pass=Config.KEY_PASS)
        if server_uptime is None:
            server_is_down = True
        return server_is_down


class PastaServer(Server):
    """
    The PastaServer uniquely identifies services provided by the Gatekeeper
    service as identified by the host name "pasta".
    """

    @staticmethod
    def check_server(host=None):
        status = Config.UP
        if PastaServer.jetty_is_down(host=host):
            status = status | Config.JETTY_DOWN
            if PastaServer.server_is_down(host=host):
                status = status | Config.SERVER_DOWN
        return status

    @staticmethod
    def jetty_is_down(host=None):
        return jetty.is_down(host=host)
