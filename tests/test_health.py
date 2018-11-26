#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_health

:Synopsis:

:Author:
    servilla
  
:Created:
    11/25/18
"""
import os
import sys
import time
import unittest

import daiquiri
import pendulum

from soh.config import Config
from soh import health_check
from soh.model.soh_db import SohDb

sys.path.insert(0, os.path.abspath('../src'))
logger = daiquiri.getLogger('test_health: ' + __name__)


class TestHealthCheck(unittest.TestCase):

    def setUp(self):
        self._soh_db = SohDb()
        self._soh_db.connect_soh_db()

    def tearDown(self):
        if os.path.exists(Config.db):
            os.remove(Config.db)

    def test_do_diagnostics(self):
        host = 'test.edirepository.org'
        now_utc = pendulum.now('UTC')

        expected = f'test.edirepository.org @ {now_utc}:\n\nSERVER DOWN\n\nJETTY DOWN\n\n'
        status = Config.assertions['SERVER_DOWN'] | Config.assertions[
            'JETTY_DOWN']
        diagnostic = health_check.do_diagnostics(host, status, now_utc)
        self.assertEqual(expected, diagnostic)

        expected = f'test.edirepository.org @ {now_utc}:\n\nIs now OK\n\n'
        status = Config.UP
        diagnostic = health_check.do_diagnostics(host, status, now_utc)
        self.assertEqual(expected, diagnostic)


if __name__ == '__main__':
    unittest.main()