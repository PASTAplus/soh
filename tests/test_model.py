#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: test_model

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
from soh.model.soh_db import SohDb

sys.path.insert(0, os.path.abspath('../src'))
logger = daiquiri.getLogger('test_model: ' + __name__)

soh_db = None


class TestModel(unittest.TestCase):

    def setUp(self):
        self._soh_db = SohDb()
        self._soh_db.connect_soh_db()

    def tearDown(self):
        if os.path.exists(Config.db):
            os.remove(Config.db)

    def test_event(self):
        now_utc = pendulum.now('UTC')
        self._soh_db.insert_soh_event(timestamp=now_utc)
        event_id = self._soh_db.get_soh_latest_event().event_id
        event_time = self._soh_db.get_soh_event_timestamp(
            event_id=event_id).timestamp
        self.assertEqual(now_utc.toordinal(), event_time.toordinal())

    def test_status(self):
        now_utc = pendulum.now('UTC')
        host = 'test.edirepository.org'
        self._soh_db.insert_soh_event(timestamp=now_utc)
        event_id = self._soh_db.get_soh_latest_event().event_id
        self._soh_db.insert_soh_status(event_id=event_id, server=host,
                                       status=str(Config.UP), timestamp=now_utc)
        status = int(self._soh_db.get_soh_latest_status_by_server(server=host).status)
        self.assertEqual(Config.UP, status)

    def test_get_latest_status_of_server(self):
        now_utc = pendulum.now('UTC')
        host = 'test.edirepository.org'
        self._soh_db.insert_soh_event(timestamp=now_utc)
        event_id = self._soh_db.get_soh_latest_event().event_id
        self._soh_db.insert_soh_status(event_id=event_id, server=host,
                                       status=str(Config.UP), timestamp=now_utc)
        time.sleep(2)
        now_utc = pendulum.now('UTC')
        host = 'test.edirepository.org'
        self._soh_db.insert_soh_event(timestamp=now_utc)
        event_id = self._soh_db.get_soh_latest_event().event_id
        self._soh_db.insert_soh_status(event_id=event_id, server=host,
                                       status=str(
                                           Config.assertions['TOMCAT_DOWN']),
                                       timestamp=now_utc)
        status = int(
            self._soh_db.get_soh_latest_status_by_server(server=host).status)
        self.assertEqual(Config.assertions['TOMCAT_DOWN'], status)


if __name__ == '__main__':
    unittest.main()
