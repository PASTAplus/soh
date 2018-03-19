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
import logging

from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Event(Base):

    __tablename__ = 'soh_event'

    event_id = Column(Integer(), primary_key=True)
    timestamp = Column(DateTime(), nullable=False)


class Test(Base):

    __tablename__ = 'soh_test'

    test_id = Column(Integer(), primary_key=True)
    test_key = Column(String(), nullable=False)
    test__name = Column(String(), nullable=False)
    test_description = Column(String(), nullable=False)


class Status(Base):

    __tablename__ = 'soh'

    status_id = Column(Integer(), primary_key=True)
    event_id = Column(Integer(), ForeignKey('soh_event.event_id'))
    server = Column(String(), nullable=False)
    status = Column(String(), nullable=False)
    timestamp = Column(DateTime(), nullable=False)
