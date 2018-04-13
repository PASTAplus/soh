#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_gmn

:Synopsis:

:Author:
    servilla
  
:Created:
    4/12/18
"""
import os
import sys
import unittest

import daiquiri

from soh.asserts import gmn
from soh.config import Config
from soh.server.server import GmnServer

logger = daiquiri.getLogger('test_gmn.py: ' + __name__)

sys.path.insert(0, os.path.abspath('../src'))

host = Config.servers['GMN_LTER']


class TestGmn(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gmn_is_down(self):
        is_down = gmn.is_down(host=host)
        self.assertIsNot(is_down, True)

    def test_GmnServer(self):
        server = GmnServer(host=host)
        status = server.check_server()
        self.assertEqual(status, Config.UP)

if __name__ == '__main__':
    unittest.main()