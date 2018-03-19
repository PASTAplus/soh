#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_jetty

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
from soh.asserts import jetty

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('test_jetty.py: ' + __name__)

sys.path.insert(0, os.path.abspath('../src'))

host = Config.PASTA_D


class TestJetty(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_jetty_is_down(self):
        is_down = jetty.is_down(host=host)
        self.assertIsNot(is_down, True)


if __name__ == '__main__':
    unittest.main()
