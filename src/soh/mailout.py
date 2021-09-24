#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: mailout

:Synopsis:

:Author:
    servilla

:Created:
    5/24/18
"""
import smtplib

import daiquiri

from soh.config import Config


logger = daiquiri.getLogger('mailout: ' + __name__)


def send_mail(subject=None, msg=None, to=None):
    result = False
    # Convert subject and msg to byte array
    body = ('Subject: ' + subject + '\n').encode() + \
           ('To: ' + ", ".join(to) + '\n').encode() + \
           ('From: ' + Config.FROM + '\n\n').encode() + \
           (msg + '\n').encode()

    smtpObj = smtplib.SMTP_SSL("mail.hover.com", 465)
    logger.warn("Created SSL smtpObj")
    try:
        smtpObj.ehlo()
        smtpObj.login(Config.HOVER_MAIL, Config.HOVER_PASSWORD)
        smtpObj.sendmail(from_addr=Config.HOVER_MAIL, to_addrs=to, msg=body)
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
