#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: health_check

:Synopsis:

:Author:
    servilla

:Created:
    3/16/18
"""
import sys

import daiquiri
from docopt import docopt
import pendulum

from soh.config import Config
from soh.lock import Lock
from soh.model.soh_db import SohDb
from soh.server.server import Server
from soh.server.server import JettyServer

logger = daiquiri.getLogger('health_check.py: ' + __name__)


def do_check(host=None, server=None, db=None, event_id=None, store=None,
             quiet=None):
    now_utc = pendulum.now('UTC')
    status = server.check_server(host=host)
    if store:
        db.insert_soh_status(event_id=event_id, server=host, status=str(status),
                             timestamp=now_utc)
    if not quiet:
        print('{host}: {status}'.format(host=host, status=status))


def main(argv):
    """
    Performs state of health checks against EDI servers/services.

    Usage:
        health_check.py all [-s | --store] [-q | --quiet]
        health_check.py production [-p | --portal] [-g | --gmn] [-s | --store]
            [-q | --quiet]
        health_check.py staging [-p | --portal] [-g | --gmn] [-s | --store]
            [-q | --quiet]
        health_check.py development [-p | --portal] [-s | --store]
            [-q | --quiet]
        health_check.py server <server> [-p | --portal] [-s | --store]
            [-q | --quiet]
        health_check.py -h | --help

    Arguments:
        all         Exam all servers
        production  Examine production tier servers
        staging     Examine staging tier servers
        development Examine development tier servers
        server      Examine specified server

    Options:
        -h --help       This page
        -p --portal     Include portals in exam
        -g --gmn        Include GMNs in exam (only production and staging)
        -s --store      Store results in SOH database
        -q --quiet      No stdout
    """
    args = docopt(str(main.__doc__))

    lock = Lock('/tmp/pastaplus_soh.lock')
    if lock.locked:
        logger.error('Lock file {} exists, exiting...'.format(lock.lock_file))
        return 1
    else:
        lock.acquire()
        logger.info('Lock file {} acquired'.format(lock.lock_file))

    # Store results in database
    store = False
    if args['--store']:
        store = True

    quiet = False
    if args['--quiet']:
        quiet = True

    soh_db = SohDb()
    soh_db.connect_soh_db()

    local_tz = pendulum.now().timezone_name
    now_utc = pendulum.now('UTC')

    event_id = None
    if store:
        soh_db.insert_soh_event(timestamp=now_utc)
        event_id_query = soh_db.get_soh_latest_event()
        if event_id_query:
            event_id = event_id_query.event_id
        else:
            msg = 'No event identifier found - aborting...'
            logger.error(msg)
            lock.release()
            logger.info('Lock file {} released'.format(lock.lock_file))
            return 1

    if args['all']:
        host = Config.servers['PASTA']
        do_check(host=host, server=JettyServer, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PACKAGE']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['AUDIT']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['SOLR']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PASTA_S']
        do_check(host=host, server=JettyServer, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PACKAGE_S']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['AUDIT_S']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['SOLR_S']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PASTA_D']
        do_check(host=host, server=JettyServer, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PACKAGE_D']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['AUDIT_D']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['SOLR_D']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PORTAL_LTER']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PORTAL_S_LTER']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PORTAL_D_LTER']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PORTAL_EDI']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PORTAL_S_EDI']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PORTAL_D_EDI']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['GMN_LTER']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['GMN_S_LTER']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['GMN_EDI']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['GMN_S_EDI']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['LDAP_EDI']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        # TODO: create special LTERLDAPSERVER test that does not do server
        # TODO: testing since the PASTA user does not exist on ldap.lternet.edu
        # host = Config.servers['LDAP_LTER']
        # do_check(host=host, server=Server, db=soh_db, event_id=event_id,
        #         store=store, quiet=quiet)

        host = Config.servers['UNIT']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['VOCAB']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

    elif args['production']:
        host = Config.servers['PASTA']
        do_check(host=host, server=JettyServer, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PACKAGE']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['AUDIT']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['SOLR']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        if args['--portal']:
            host = Config.servers['PORTAL_LTER']
            do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                     store=store, quiet=quiet)

            host = Config.servers['PORTAL_EDI']
            do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                     store=store, quiet=quiet)

        if args['--gmn']:
            host = Config.servers['GMN_LTER']
            do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                     store=store, quiet=quiet)

            host = Config.servers['GMN_EDI']
            do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                     store=store, quiet=quiet)

    elif args['staging']:
        host = Config.servers['PASTA_S']
        do_check(host=host, server=JettyServer, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PACKAGE_S']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['AUDIT_S']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['SOLR_S']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        if args['--portal']:
            host = Config.servers['PORTAL_S_LTER']
            do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                     store=store, quiet=quiet)

            host = Config.servers['PORTAL_S_EDI']
            do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                     store=store, quiet=quiet)

        if args['--gmn']:
            host = Config.servers['GMN_S_LTER']
            do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                     store=store, quiet=quiet)

            host = Config.servers['GMN_S_EDI']
            do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                     store=store, quiet=quiet)

    elif args['development']:
        host = Config.servers['PASTA_D']
        do_check(host=host, server=JettyServer, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['PACKAGE_D']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['AUDIT_D']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        host = Config.servers['SOLR_D']
        do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                 store=store, quiet=quiet)

        if args['--portal']:
            host = Config.servers['PORTAL_D_LTER']
            do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                     store=store, quiet=quiet)

            host = Config.servers['PORTAL_D_EDI']
            do_check(host=host, server=Server, db=soh_db, event_id=event_id,
                     store=store, quiet=quiet)

    lock.release()
    logger.info('Lock file {} released'.format(lock.lock_file))

    return 0


if __name__ == "__main__":
    main(sys.argv)
