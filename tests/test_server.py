#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_server

:Synopsis:

:Author:
    servilla
  
:Created:
    3/16/18
"""
import logging
import os
import sys
import unittest

import daiquiri

from soh.config import Config
from soh.server.server import Server


daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('test_server.py: ' + __name__)


sys.path.insert(0, os.path.abspath('../src'))

host = Config.PASTA_D


class TestServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_test_server(self):
        status = Server.test_server(host=host)
        self.assertEqual(status, Config.UP)



if __name__ == '__main__':
    unittest.main()