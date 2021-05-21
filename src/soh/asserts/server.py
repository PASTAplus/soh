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
    except asyncssh.TimeoutError as e:
        logger.error(e)
    except asyncssh.ProcessError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)
    return uptime


async def read_only(host=None):
    port = 22
    cmd = 'touch /tmp/ro_test; rm /tmp/ro_test'

    ro = True

    try:
        async with asyncssh.connect(host=host, port=port) as conn:
            result = await conn.run(cmd, check=True)
            if result.exit_status == 0:
                ro = False

    except asyncssh.ChannelOpenError as e:
        logger.error(e)
    except asyncssh.TimeoutError as e:
        logger.error(e)
    except asyncssh.ProcessError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)
    return ro
