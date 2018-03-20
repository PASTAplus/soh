#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: uptime

:Synopsis:

:Author:
    servilla

:Created:
    3/12/18
"""

import logging

import daiquiri
import paramiko

logger = daiquiri.getLogger('server.py: ' + __name__)


def uptime(host=None, user=None, key_path=None, key_pass=None):
    port = 22
    cmd = 'uptime'

    uptime = None

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    try:
        client.connect(hostname=host, port=port, username=user,
                       key_filename=key_path, passphrase=key_pass, timeout=5.0,
                       auth_timeout=5.0)

        stdin, stdout, stderr = client.exec_command(command=cmd)
        line = ''.join([_.strip() for _ in stdout.readlines()])
        if line and 'load average:' in line:
            uptime = line

    except paramiko.AuthenticationException as e:
        logger.error(e)
    except paramiko.BadHostKeyException as e:
        logger.error(e)
    except paramiko.SSHException as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)
    finally:
        client.close()
    return uptime
