#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_tomcat

:Synopsis:

:Author:
    servilla
  
:Created:
    3/30/18
"""
import os
import sys
import unittest

import daiquiri

from soh.config import Config
from soh.asserts import tomcat
from soh.server.server import TomcatServer

logger = daiquiri.getLogger('test_tomcat.py: ' + __name__)

sys.path.insert(0, os.path.abspath('../src'))

host = Config.servers['PACKAGE_D']

class TestTomcat(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_tomcat_is_down(self):
        is_down = tomcat.is_down(host=host)
        self.assertIsNot(is_down, True)

    def test_Tomcat(self):
        server = TomcatServer(host=host)
        status = server.check_server()
        self.assertEqual(status, Config.UP)


if __name__ == '__main__':
    unittest.main()