#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: mailout

:Synopsis:

:Author:
    servilla

:Created:
    5/24/18
"""
from email.utils import formataddr
import smtplib

import daiquiri

from soh.config import Config


logger = daiquiri.getLogger('mailout: ' + __name__)


def send_mail(subject=None, msg=None, to=None):
    result = False
    # Convert subject and msg to byte array
    body = ('Subject: ' + subject + '\n').encode() + \
           ('To: ' + formataddr(("Admin", to)) + '\n').encode() + \
           ('From: ' + formataddr(("Dashboard", Config.FROM)) + '\n\n').encode() + \
           (msg + '\n').encode()

    smtpObj = smtplib.SMTP(Config.RELAY_HOST, Config.RELAY_TLS_PORT)
    smtpObj.starttls()
    logger.warn("Created SSL smtpObj")
    try:
        smtpObj.ehlo()
        smtpObj.login(Config.RELAY_USER, Config.RELAY_PASSWORD)
        smtpObj.sendmail(from_addr=Config.FROM, to_addrs=to, msg=body)
        result = True
        logger.warn(f"Sending email to: {to}")
    except Exception as e:
        response = 'Sending email failed - ' + str(e)
        logger.error(response)
    finally:
        smtpObj.quit()
    return result


def main():
    return 0


if __name__ == "__main__":
    main()
