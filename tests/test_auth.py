#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_auth

:Synopsis:

:Author:
    servilla
  
:Created:
    10/25/19
"""
import os
import sys
import unittest

import daiquiri

from soh.config import Config
from soh.asserts import auth
from soh.server.server import AuthServer

logger = daiquiri.getLogger('test_auth.py: ' + __name__)

sys.path.insert(0, os.path.abspath('../src'))

host = Config.servers['AUTH']


class TestAuth(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_auth_is_down(self):
        is_down = auth.is_down(host=host)
        self.assertIsNot(is_down, True)

    def test_Auth(self):
        server = AuthServer(host=host)
        status = server.check_server()
        self.assertEqual(status, Config.UP)


if __name__ == '__main__':
    unittest.main()
