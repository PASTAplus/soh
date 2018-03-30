#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_jetty

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

from soh.asserts import jetty
from soh.config import Config
from soh.server.server import JettyServer

logger = daiquiri.getLogger('test_jetty.py: ' + __name__)

sys.path.insert(0, os.path.abspath('../src'))

host = Config.servers['PASTA_D']


class TestJetty(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_jetty_is_down(self):
        is_down = jetty.is_down(host=host)
        self.assertIsNot(is_down, True)

    def test_Jetty(self):
        status = JettyServer.check_server(host=host)
        self.assertEqual(status, Config.UP)


if __name__ == '__main__':
    unittest.main()
