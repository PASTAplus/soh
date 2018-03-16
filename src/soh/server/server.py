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
from soh.tests import uptime

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('server.py: ' + __name__)


class Server(object):

    def __init__(self, host=None):
        self._status = 0
        self._host = host

    def test_server(self):
        # Test server uptime
        server_uptime = uptime.check_uptime(host=self._host, user=Config.user,
                               key_path=Config.key_path,
                               key_pass=Config.key_pass)
        if server_uptime is None:
            self._status = self._status | Config.tests['uptime']

    @property
    def status(self):
        return self._status

def main():
    return 0


if __name__ == "__main__":
    main()
