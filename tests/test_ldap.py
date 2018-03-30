#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_ldap

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

from soh.asserts import ldap
from soh.config import Config
from soh.server.server import LdapServer

logger = daiquiri.getLogger('test_ldap.py: ' + __name__)

sys.path.insert(0, os.path.abspath('../src'))

host = Config.servers['LDAP_EDI']


class TestModuleName(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ldap_is_down(self):
        is_down = ldap.is_down(host=host)
        self.assertIsNot(is_down, True)

    def test_Ldap(self):
        status = LdapServer.check_server(host=host)
        self.assertEqual(status, Config.UP)


if __name__ == '__main__':
    unittest.main()