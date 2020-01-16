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

import click
import daiquiri
from docopt import docopt
import pendulum

from soh.config import Config
from soh.lock import Lock
from soh import mailout
from soh.model.soh_db import SohDb
from soh.server.server import ApacheServer
from soh.server.server import ApacheTomcatServer
from soh.server.server import AuditServer
from soh.server.server import AuthServer
from soh.server.server import GmnServer
from soh.server.server import JettyServer
from soh.server.server import LdapServer
from soh.server.server import PackageServer
from soh.server.server import PortalServer
from soh.server.server import Server
from soh.server.server import SolrServer
from soh.server.server import TomcatServer

logger = daiquiri.getLogger('health_check.py: ' + __name__)


def do_check(host=None, db=None, event_id=None, store=None, quiet=None, notify=None):
    now_utc = pendulum.now('UTC')

    server = None
    if host in Config.server_types['APACHE']:
        server = ApacheServer(host=host)
    elif host in Config.server_types['APACHE_TOMCAT']:
        server = ApacheTomcatServer(host=host)
    elif host in Config.server_types['AUDIT']:
        server = AuditServer(host=host)
    elif host in Config.server_types['AUTH']:
        server = AuthServer(host=host)
    elif host in Config.server_types['GMN']:
        server = GmnServer(host=host)
    elif host in Config.server_types['JETTY']:
        server = JettyServer(host=host)
    elif host in Config.server_types['LDAP']:
        server = LdapServer(host=host)
    elif host in Config.server_types['PACKAGE']:
        server = PackageServer(host=host)
    elif host in Config.server_types['PORTAL']:
        server = PortalServer(host=host)
    elif host in Config.server_types['SERVER']:
        server = Server(host=host)
    elif host in Config.server_types['SOLR']:
        server = SolrServer(host=host)
    elif host in Config.server_types['TOMCAT']:
        server = TomcatServer(host=host)
    else:
        logger.error('Unknown server: {host}'.format(host=host))
        return

    status = server.check_server()

    if notify:
        prior_status = db.get_soh_latest_status_by_server(host)
        if prior_status is not None and int(prior_status.status) != status:
            diagnostic = do_diagnostics(host, status, now_utc)
            subject = f'Status change for {host}'
            try:
                mailout.send_mail(subject=subject, msg=diagnostic, to=Config.ADMIN_TO)
            except Exception as e:
                logger.error(e)

    if store:
        db.insert_soh_status(event_id=event_id, server=host, status=str(status),
                             timestamp=now_utc)
    if not quiet:
        print('{host}: {status}'.format(host=host, status=status))


def do_diagnostics(host: str, status: int, timestamp: pendulum.datetime) -> str:

    local_time = timestamp.in_timezone('America/Denver').to_datetime_string()

    diagnostics = f'{host} @ {timestamp} ({local_time} MT):\n'

    if status == Config.UP:
        diagnostics += 'Is now OK\n'

    if status & Config.assertions['SERVER_DOWN']:
        diagnostics += 'SERVER DOWN\n'

    if status & Config.assertions['JETTY_DOWN']:
        diagnostics += 'JETTY DOWN\n'

    if status & Config.assertions['TOMCAT_DOWN']:
        diagnostics += 'TOMCAT DOWN\n'

    if status & Config.assertions['SOLR_DOWN']:
        diagnostics += 'SOLR DOWN\n'

    if status & Config.assertions['LDAP_DOWN']:
        diagnostics += 'LDAP DOWN\n'

    if status & Config.assertions['APACHE_DOWN']:
        diagnostics += 'APACHE DOWN\n'

    if status & Config.assertions['GMN_DOWN']:
        diagnostics += 'GMN DOWN\n'

    if status & Config.assertions['PORTAL_DOWN']:
        diagnostics += 'PORTAL DOWN\n'

    if status & Config.assertions['PACKAGE_DOWN']:
        diagnostics += 'PACKAGE DOWN\n'

    if status & Config.assertions['GATEKEEPER_DOWN']:
        diagnostics += 'GATEKEEPER DOWN\n'

    if status & Config.assertions['AUDIT_DOWN']:
        diagnostics += 'AUDIT DOWN\n'

    if status & Config.assertions['AUTH_DOWN']:
        diagnostics += 'AUTH DOWN\n'

    return diagnostics


help_store = "Store results in SOH database"
help_quiet = "No stdout"
help_notify = "Send email notification of server status change"


@click.command()
@click.argument('hosts', nargs=-1)
@click.option('-s', '--store', default=False, is_flag=True, help=help_store)
@click.option('-q', '--quiet', default=False, is_flag=True, help=help_quiet)
@click.option('-n', '--notify', default=False, is_flag=True, help=help_notify)
def main(hosts: tuple, store: bool, quiet: bool, notify: bool):
    """
    Performs state of health checks against EDI servers/services.

    \b
    HOSTS: space separated list of hosts

    """

    lock = Lock(Config.LOCK_FILE)
    if lock.locked:
        logger.error('Lock file {} exists, exiting...'.format(lock.lock_file))
        return 1
    else:
        lock.acquire()
        logger.info('Lock file {} acquired'.format(lock.lock_file))

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

    if len(hosts) == 0:
        msg = "No hosts specified"
        logger.warning(msg)
    else:
        for host in hosts:
            do_check(host=host, db=soh_db, event_id=event_id, store=store,
                     quiet=quiet, notify=notify)

    lock.release()
    logger.info('Lock file {} released'.format(lock.lock_file))

    return 0


if __name__ == "__main__":
    main()
