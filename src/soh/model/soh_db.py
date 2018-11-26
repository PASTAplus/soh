#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: soh_db

:Synopsis:
    Model for PASTA State of Health events

:Author:
    servilla

:Created:
    3/18/18
"""
import daiquiri
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, desc, asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from soh.config import Config

logger = daiquiri.getLogger('soh_db.py: ' + __name__)

Base = declarative_base()


class SohEvent(Base):
    __tablename__ = 'soh_event'

    event_id = Column(Integer(), primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(), nullable=False)


class SohAssert(Base):
    __tablename__ = 'soh_assert'

    assert_id = Column(Integer(), primary_key=True, autoincrement=True)
    assert_key = Column(String(), nullable=False)
    assert_name = Column(String(), nullable=False)
    assert_description = Column(String(), nullable=False)


class SohStatus(Base):
    __tablename__ = 'soh_status'

    status_id = Column(Integer(), primary_key=True, autoincrement=True)
    event_id = Column(Integer(), ForeignKey('soh_event.event_id'))
    server = Column(String(), nullable=False)
    status = Column(String(), nullable=False)
    timestamp = Column(DateTime(), nullable=False)


class SohDb(object):

    def __init__(self, db_name=Config.db):
        self._db_name = db_name

    def connect_soh_db(self):
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///' + self._db_name)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def insert_soh_event(self, timestamp=None):
        record = SohEvent(timestamp=timestamp)
        self.session.add(record)
        self.session.commit()

    def insert_soh_status(self, event_id=None, server=None, status=None,
                          timestamp=None):
        record = SohStatus(event_id=event_id, server=server, status=status,
                           timestamp=timestamp)
        self.session.add(record)
        self.session.commit()

    def get_soh_latest_event(self):
        """
        Return the latest event identifier.
        :return: Query or None
        """
        return self.session.query(SohEvent).order_by(
            desc(SohEvent.timestamp)).first()

    def get_soh_event_timestamp(self, event_id=None):
        """
        Return timestamp of given event described by event_id.
        :param event_id:
        :return: Query or passes on NoResultFound exception
        """
        return self.session.query(SohEvent).filter(
            SohEvent.event_id == event_id).one()

    def get_soh_latest_status_by_server(self, server=None):
        """
        Return latest status for the given server.
        :param server:
        :return: Query or None
        """
        return self.session.query(SohStatus).filter(
            SohStatus.server == server).order_by(
            desc(SohStatus.event_id)).first()

    def get_soh_status_by_event(self, event_id=None):
        """
        Return all statuses for the event described by event_id.
        :param event_id:
        :return: Iterable query or None
        """
        return self.session.query(SohStatus).filter(
            SohStatus.event_id == event_id)

    def get_soh_status_by_server(self, server=None):
        """
        Return all statuses for the given server.
        :param server:
        :return: Iterable query or None
        """
        return self.session.query(SohStatus).filter(
            SohStatus.server == server).order_by(asc(SohStatus.event_id))
