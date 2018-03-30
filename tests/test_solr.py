#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_solr

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

from soh.asserts import solr
from soh.config import Config
from soh.server.server import SolrServer

logger = daiquiri.getLogger('test_solr.py: ' + __name__)

sys.path.insert(0, os.path.abspath('../src'))

host = Config.servers['SOLR_D']


class TestSolr(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_solr_is_down(self):
        is_down = solr.is_down(host=host)
        self.assertIsNot(is_down, True)

    def test_Solr(self):
        server = SolrServer(host=host)
        status = server.check_server()
        self.assertEqual(status, Config.UP)


if __name__ == '__main__':
    unittest.main()