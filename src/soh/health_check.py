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
from soh.server.server import Server
from soh.server.server import PastaServer

daiquiri.setup(level=logging.WARN)
logger = daiquiri.getLogger('health_check.py: ' + __name__)


def main(argv):
    """
    Performs state of health checks against EDI servers/services.

    Usage:
        health_check.py all
        health_check.py production [-p | --portal] [-g | --gmn]
        health_check.py staging [-p | --portal] [-g | --gmn]
        health_check.py development [-p | --portal]
        health_check.py -h | --help

    Arguments:
        all         Exam all servers
        production  Examine production tier servers
        staging     Examine staging tier servers
        development Examine development tier servers

    Options:
        -h --help       This page
        -p --portal     Include portals in exam
        -g --gmn        Include GMNs in exam (only production and staging)
    """

    args = docopt(str(main.__doc__))

    if args['all']:
        host = Config.PASTA
        status = PastaServer.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PACKAGE
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.AUDIT
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.SOLR
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PASTA_S
        status = PastaServer.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PACKAGE_S
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.AUDIT_S
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.SOLR_S
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PASTA_D
        status = PastaServer.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PACKAGE_D
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.AUDIT_D
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.SOLR_D
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PORTAL_LTER
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PORTAL_S_LTER
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PORTAL_D_LTER
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PORTAL_EDI
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PORTAL_S_EDI
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PORTAL_D_EDI
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.GMN_LTER
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.GMN_S_LTER
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.GMN_EDI
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.GMN_S_EDI
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.LDAP_EDI
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        # TODO: create special LTERLDAPSERVER test that does not do server
        # TODO: testing since the PASTA user does not exist on ldap.lternet.edu
        # host = Config.LDAP_LTER
        # status = Server.test_server(host=host)
        # print('{host}: {status}'.format(host=host, status=status))

        host = Config.UNIT
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.VOCAB
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

    elif args['production']:
        host = Config.PASTA
        status = PastaServer.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PACKAGE
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.AUDIT
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.SOLR
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        if args['--portal']:
            host = Config.PORTAL_LTER
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))

            host = Config.PORTAL_EDI
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))

        if args['--gmn']:
            host = Config.GMN_LTER
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))

            host = Config.GMN_EDI
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))

    elif args['staging']:
        host = Config.PASTA_S
        status = PastaServer.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PACKAGE_S
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.AUDIT_S
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.SOLR_S
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        if args['--portal']:
            host = Config.PORTAL_S_LTER
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))

            host = Config.PORTAL_S_EDI
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))

        if args['--gmn']:
            host = Config.GMN_S_LTER
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))

            host = Config.GMN_S_EDI
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))

    elif args['development']:
        host = Config.PASTA_D
        status = PastaServer.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.PACKAGE_D
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.AUDIT_D
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        host = Config.SOLR_D
        status = Server.test_server(host=host)
        print('{host}: {status}'.format(host=host, status=status))

        if args['--portal']:
            host = Config.PORTAL_D_LTER
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))

            host = Config.PORTAL_D_EDI
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))



    return 0


if __name__ == "__main__":
    main(sys.argv)
