#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_email

:Synopsis:

:Author:
    servilla

:Created:
    5/9/22
"""
import pytest

import soh.mimemail


def test_mimemail():
    subject = "Test"
    message = "Testing email"

    assert(soh.mimemail.send_mail(subject, message) is True)
