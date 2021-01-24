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
import os
import pickle
import re
import sys
import time
from typing import List

import click
import daiquiri
import pendulum

from soh.config import Config
from soh.lock import Lock
from soh import mailout
from soh.asserts import server
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

cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + "/health_check.log"
daiquiri.setup(level=logging.WARN, outputs=(daiquiri.output.File(logfile),
                                            "stdout"))

logger = daiquiri.getLogger("health_check.py: " + __name__)


def do_check(host=None):
    now_utc = pendulum.now("UTC")

    server = None
    if host in Config.server_types["APACHE"]:
        server = ApacheServer(host=host)
    elif host in Config.server_types["APACHE_TOMCAT"]:
        server = ApacheTomcatServer(host=host)
    elif host in Config.server_types["AUDIT"]:
        server = AuditServer(host=host)
    elif host in Config.server_types["AUTH"]:
        server = AuthServer(host=host)
    elif host in Config.server_types["GMN"]:
        server = GmnServer(host=host)
    elif host in Config.server_types["JETTY"]:
        server = JettyServer(host=host)
    elif host in Config.server_types["LDAP"]:
        server = LdapServer(host=host)
    elif host in Config.server_types["PACKAGE"]:
        server = PackageServer(host=host)
    elif host in Config.server_types["PORTAL"]:
        server = PortalServer(host=host)
    elif host in Config.server_types["SERVER"]:
        server = Server(host=host)
    elif host in Config.server_types["SOLR"]:
        server = SolrServer(host=host)
    elif host in Config.server_types["TOMCAT"]:
        server = TomcatServer(host=host)
    else:
        logger.error(f"Unknown server: {host}")
        return

    status = server.check_server()
    return status


def do_diagnostics(host: str, status: int, uptime: str, timestamp: pendulum.datetime) -> str:
    local_time = timestamp.in_timezone("America/Denver").to_datetime_string()

    diagnostics = f"{host} @ {timestamp} ({local_time} MT):\n"
    diagnostics += f"Uptime: {uptime}\n"

    if status == Config.UP:
        diagnostics += "Is now OK\n"

    if status & Config.assertions["SERVER_DOWN"]:
        diagnostics += "SERVER DOWN\n"

    if status & Config.assertions["JETTY_DOWN"]:
        diagnostics += "JETTY DOWN\n"

    if status & Config.assertions["TOMCAT_DOWN"]:
        diagnostics += "TOMCAT DOWN\n"

    if status & Config.assertions["SOLR_DOWN"]:
        diagnostics += "SOLR DOWN\n"

    if status & Config.assertions["LDAP_DOWN"]:
        diagnostics += "LDAP DOWN\n"

    if status & Config.assertions["APACHE_DOWN"]:
        diagnostics += "APACHE DOWN\n"

    if status & Config.assertions["GMN_DOWN"]:
        diagnostics += "GMN DOWN\n"

    if status & Config.assertions["PORTAL_DOWN"]:
        diagnostics += "PORTAL DOWN\n"

    if status & Config.assertions["PACKAGE_DOWN"]:
        diagnostics += "PACKAGE DOWN\n"

    if status & Config.assertions["GATEKEEPER_DOWN"]:
        diagnostics += "GATEKEEPER DOWN\n"

    if status & Config.assertions["AUDIT_DOWN"]:
        diagnostics += "AUDIT DOWN\n"

    if status & Config.assertions["AUTH_DOWN"]:
        diagnostics += "AUTH DOWN\n"

    if status & Config.assertions["SYNC_DOWN"]:
        diagnostics += "SYNC DOWN\n"

    if status & Config.assertions["LOAD_HIGH"]:
        diagnostics += "LOAD HIGH\n"

    return diagnostics


def get_load(uptime: str):
    load = None
    if uptime is not None:
        match = re.search(r"\d?\d\.\d\d, \d?\d\.\d\d, \d?\d\.\d\d", uptime)
        if match:
            load = [float(_.strip()) for _ in match.group().split(",")]
    return load


def load_status(load: List) -> int:
    status = Config.UP
    if load is None:
        status = Config.assertions["LOAD_HIGH"]
    else:
        load1 = load[0]
        load5 = load[1]
        load15 = load[2]
        if load1 >= Config.LOAD1_MAX:
            status = Config.assertions["LOAD_HIGH"]
    return status


help_store = "Store results in SOH database"
help_quiet = "No stdout"
help_notify = "Send email notification of server status change"


@click.command()
@click.argument("hosts", nargs=-1)
@click.option("-s", "--store", default=False, is_flag=True, help=help_store)
@click.option("-q", "--quiet", default=False, is_flag=True, help=help_quiet)
@click.option("-n", "--notify", default=False, is_flag=True, help=help_notify)
def main(hosts: tuple, store: bool, quiet: bool, notify: bool):
    """
    Performs state of health checks against EDI servers/services.

    \b
    HOSTS: space separated list of hosts

    """
    new_status = dict()
    if os.path.exists(Config.STATUS_FILE):
        with open(Config.STATUS_FILE, "rb") as f:
            old_status = pickle.load(f)
    else:
        old_status = dict()

    lock = Lock(Config.LOCK_FILE)
    if lock.locked:
        msg = f"Lock file {lock.lock_file} exists, exiting..."
        logger.error(msg)
        try:
            subject = f"Dashboard: Lock file {lock.lock_file} exists..."
            mailout.send_mail(
                subject=subject, msg=msg, to=Config.ADMIN_TO
            )
        except Exception as e:
            logger.error(e)
        return 1
    else:
        lock.acquire()
        logger.info(f"Lock file {lock.lock_file} acquired")

    soh_db = SohDb()
    soh_db.connect_soh_db()

    local_tz = pendulum.now().timezone_name
    now_utc = pendulum.now("UTC")
    new_status["timestamp"] = now_utc.isoformat()

    if len(hosts) == 0:
        msg = "No hosts specified"
        logger.warning(msg)
    else:
        for host in hosts:
            host_status = do_check(host=host)
            host_uptime = server.uptime(
                host=host,
                user=Config.USER,
                key_path=Config.KEY_PATH,
                key_pass=Config.KEY_PASS
            )
            if host_uptime is not None:
                host_status = host_status | load_status(get_load(host_uptime))
            if notify:
                if host not in old_status or old_status[host][0] != host_status:
                    diagnostic = do_diagnostics(host, host_status, host_uptime, now_utc)
                    subject = f"Status change for {host}"
                    logger.warning(diagnostic)
                    try:
                        mailout.send_mail(
                            subject=subject, msg=diagnostic, to=Config.ADMIN_TO
                        )
                    except Exception as e:
                        logger.error(e)
            if store:
                new_status[host] = (host_status, host_uptime)
                with open(Config.STATUS_FILE, "wb") as f:
                    pickle.dump(new_status, f)
            if not quiet:
                print(f"{host}: {host_status} - {host_uptime}")
            time.sleep(Config.SLEEP)
    lock.release()
    logger.info("Lock file {} released".format(lock.lock_file))

    sys.exit(0)


if __name__ == "__main__":
    main()
