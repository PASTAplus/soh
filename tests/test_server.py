#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: check_server

:Synopsis:

:Author:
    servilla
  
:Created:
    3/16/18
"""
import os
import sys
import unittest

import daiquiri

from soh.asserts import server
from soh.config import Config
from soh.server.server import Server


logger = daiquiri.getLogger('test_server.py: ' + __name__)


sys.path.insert(0, os.path.abspath('../src'))

host = Config.servers['PASTA_D']


class TestServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_server_uptime(self):
        user = Config.USER
        key_path = Config.KEY_PATH
        key_pass = Config.KEY_PASS
        uptime = server.uptime(host=host, user=user, key_path=key_path,
                               key_pass=key_pass)
        self.assertIsNotNone(uptime)

    def test_Server(self):
        server = Server(host=host)
        status = server.check_server()
        self.assertEqual(status, Config.UP)



if __name__ == '__main__':
    unittest.main()