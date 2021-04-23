#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: uptime

:Synopsis:

:Author:
    servilla

:Created:
    3/12/18
"""
import asyncssh
import daiquiri
import paramiko

logger = daiquiri.getLogger('server.py: ' + __name__)


async def uptime(host=None):
    port = 22
    cmd = 'uptime'

    uptime = None

    try:
        async with asyncssh.connect(host=host, port=port) as conn:
            result = await conn.run(cmd, check=True)
            line = result.stdout.strip()
            if line and 'load average:' in line:
                uptime = line

    except asyncssh.ChannelOpenError as e:
        logger.error(e)
    except asyncssh.ProcessError as e:
        logger.error(e)
    except asyncssh.TimeoutError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)
    return uptime
