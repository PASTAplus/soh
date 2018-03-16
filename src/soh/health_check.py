#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: health_check

:Synopsis:

:Author:
    servilla

:Created:
    3/16/18
"""

import logging
import sys

import daiquiri
from docopt import docopt

from soh.config import Config

daiquiri.setup(level=logging.INFO)
logger = daiquiri.getLogger('health_check.py: ' + __name__)


def main(argv):
    """
    Performs state of health checks against EDI servers/services.

    Usage:
        health_check.py all
        health_check.py production [-p | --portal] [-g | --gmn]
        health_check.py staging [-p | --portal] [-g | --gmn]
        health_check.py development [-p | --portal] [-g | --gmn]
        health_check.py -h | --help

    Arguments:
        all         Exam all servers
        production  Examine production tier servers
        staging     Examine staging tier servers
        development Examine development tier servers

    Options:
        -h --help       This page
        -p --portal     Include portals in exam
        -g --gmn        Include GMNs in exam
    """

    args = docopt(str(main.__doc__))

    servers = []

    if args['all']:
        for server in Config.servers:
            servers.append(server)
    elif args['production']:
        servers = ['pasta', 'package', 'audit', 'solr']
        if args['--portal']:
            servers.append('portal_lter')
            servers.append('portal_edi')
        if args['--gmn']:
            servers.append('gmn_lter')
            servers.append('gmn_edi')

    return 0


if __name__ == "__main__":
    main(sys.argv)
