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
import pendulum

from soh.config import Config
from soh.model.soh_db import SohDb
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

    soh_db = SohDb()
    soh_db.connect_soh_db()

    now_utc = pendulum.now('UTC')
    soh_db.insert_soh_event(timestamp=now_utc)
    event_id_query = soh_db.get_soh_latest_event()

    if event_id_query:
        event_id = event_id_query.event_id

        if args['all']:
            host = Config.PASTA
            now_utc = pendulum.now('UTC')
            status = PastaServer.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PACKAGE
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.AUDIT
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.SOLR
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PASTA_S
            now_utc = pendulum.now('UTC')
            status = PastaServer.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PACKAGE_S
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.AUDIT_S
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.SOLR_S
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PASTA_D
            now_utc = pendulum.now('UTC')
            status = PastaServer.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PACKAGE_D
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.AUDIT_D
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.SOLR_D
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PORTAL_LTER
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PORTAL_S_LTER
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PORTAL_D_LTER
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PORTAL_EDI
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PORTAL_S_EDI
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PORTAL_D_EDI
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.GMN_LTER
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.GMN_S_LTER
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.GMN_EDI
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.GMN_S_EDI
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.LDAP_EDI
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            # TODO: create special LTERLDAPSERVER test that does not do server
            # TODO: testing since the PASTA user does not exist on ldap.lternet.edu
            # host = Config.LDAP_LTER
            # now_utc = pendulum.now('UTC')
            # status = Server.test_server(host=host)
            # print('{host}: {status}'.format(host=host, status=status))
            # soh_db.insert_soh_status(event_id=event_id, server=host,
            #                          status=str(status), timestamp=now_utc)

            host = Config.UNIT
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.VOCAB
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

        elif args['production']:
            host = Config.PASTA
            now_utc = pendulum.now('UTC')
            status = PastaServer.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PACKAGE
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.AUDIT
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.SOLR
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            if args['--portal']:
                host = Config.PORTAL_LTER
                now_utc = pendulum.now('UTC')
                status = Server.test_server(host=host)
                print('{host}: {status}'.format(host=host, status=status))
                soh_db.insert_soh_status(event_id=event_id, server=host,
                                         status=str(status), timestamp=now_utc)

                host = Config.PORTAL_EDI
                now_utc = pendulum.now('UTC')
                status = Server.test_server(host=host)
                print('{host}: {status}'.format(host=host, status=status))
                soh_db.insert_soh_status(event_id=event_id, server=host,
                                         status=str(status), timestamp=now_utc)

            if args['--gmn']:
                host = Config.GMN_LTER
                now_utc = pendulum.now('UTC')
                status = Server.test_server(host=host)
                print('{host}: {status}'.format(host=host, status=status))
                soh_db.insert_soh_status(event_id=event_id, server=host,
                                         status=str(status), timestamp=now_utc)

                host = Config.GMN_EDI
                now_utc = pendulum.now('UTC')
                status = Server.test_server(host=host)
                print('{host}: {status}'.format(host=host, status=status))
                soh_db.insert_soh_status(event_id=event_id, server=host,
                                         status=str(status), timestamp=now_utc)

        elif args['staging']:
            host = Config.PASTA_S
            now_utc = pendulum.now('UTC')
            status = PastaServer.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PACKAGE_S
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.AUDIT_S
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.SOLR_S
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            if args['--portal']:
                host = Config.PORTAL_S_LTER
                now_utc = pendulum.now('UTC')
                status = Server.test_server(host=host)
                print('{host}: {status}'.format(host=host, status=status))
                soh_db.insert_soh_status(event_id=event_id, server=host,
                                         status=str(status), timestamp=now_utc)

                host = Config.PORTAL_S_EDI
                now_utc = pendulum.now('UTC')
                status = Server.test_server(host=host)
                print('{host}: {status}'.format(host=host, status=status))
                soh_db.insert_soh_status(event_id=event_id, server=host,
                                         status=str(status), timestamp=now_utc)

            if args['--gmn']:
                host = Config.GMN_S_LTER
                now_utc = pendulum.now('UTC')
                status = Server.test_server(host=host)
                print('{host}: {status}'.format(host=host, status=status))
                soh_db.insert_soh_status(event_id=event_id, server=host,
                                         status=str(status), timestamp=now_utc)

                host = Config.GMN_S_EDI
                now_utc = pendulum.now('UTC')
                status = Server.test_server(host=host)
                print('{host}: {status}'.format(host=host, status=status))
                soh_db.insert_soh_status(event_id=event_id, server=host,
                                         status=str(status), timestamp=now_utc)

        elif args['development']:
            host = Config.PASTA_D
            now_utc = pendulum.now('UTC')
            status = PastaServer.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.PACKAGE_D
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.AUDIT_D
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            host = Config.SOLR_D
            now_utc = pendulum.now('UTC')
            status = Server.test_server(host=host)
            print('{host}: {status}'.format(host=host, status=status))
            soh_db.insert_soh_status(event_id=event_id, server=host,
                                     status=str(status), timestamp=now_utc)

            if args['--portal']:
                host = Config.PORTAL_D_LTER
                now_utc = pendulum.now('UTC')
                status = Server.test_server(host=host)
                print('{host}: {status}'.format(host=host, status=status))
                soh_db.insert_soh_status(event_id=event_id, server=host,
                                         status=str(status), timestamp=now_utc)

                host = Config.PORTAL_D_EDI
                now_utc = pendulum.now('UTC')
                status = Server.test_server(host=host)
                print('{host}: {status}'.format(host=host, status=status))
                soh_db.insert_soh_status(event_id=event_id, server=host,
                                         status=str(status), timestamp=now_utc)

    else:
        logger.warn('No event identifier available - aborting...')

    return 0


if __name__ == "__main__":
    main(sys.argv)
