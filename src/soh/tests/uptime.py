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
import sys

import daiquiri
from docopt import docopt
import paramiko


daiquiri.setup(level=logging.WARN)
logger = daiquiri.getLogger('uptime.py: ' + __name__)


def check_uptime(host=None, user=None, key_path=None, key_pass=None):
    port = 22
    cmd = 'uptime'

    uptime = None

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    try:
        client.connect(hostname=host, port=port, username=user,
                       key_filename=key_path, passphrase=key_pass)

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


def main(argv):
    """
    Performs state of health checks against PASTA-based servers/services.

    Usage:
        health_check.py uptime (-H | --Hosts <hosts>) (-u | --user <user>)
            (-k | --key <key_path>) (-p | --pass <key_pass>)
        health_check.py -h | --help

    Options:
        -h --help   This page
        -H --Hosts  A comma delimited list of host names or IP addresses \
                    without spaces between commas
        -u --user   User name for authentication
        -k --key    SSH key file path
        -p --pass   SSH key file pass phrase

    """
    args = docopt(str(main.__doc__))

    if args['uptime']:
        hosts = [_.strip() for _ in args['<hosts>'].split(',')]
        user = args['<user>'].strip()
        key_path = args['<key_path>'].strip()
        key_pass = args['<key_pass>'].strip()
        for host in hosts:
            uptime = check_uptime(host=host, user=user, key_path=key_path,
                                  key_pass=key_pass)
            if uptime is not None:
                print('{host}: {uptime}'.format(host=host, uptime=uptime))
            else:
                print('{host}: is not up'.format(host=host))

    return 0


if __name__ == "__main__":
    main(sys.argv)
