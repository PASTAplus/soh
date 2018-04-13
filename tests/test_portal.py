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

from soh.asserts import portal
from soh.config import Config
from soh.server.server import PortalServer

logger = daiquiri.getLogger('test_portal.py: ' + __name__)

sys.path.insert(0, os.path.abspath('../src'))

host = Config.servers['PORTAL_D_EDI']


class TestPortal(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_portal_is_down(self):
        is_down = portal.is_down(host=host)
        self.assertIsNot(is_down, True)

    def test_PortalServer(self):
        server = PortalServer(host=host)
        status = server.check_server()
        self.assertEqual(status, Config.UP)

if __name__ == '__main__':
    unittest.main()