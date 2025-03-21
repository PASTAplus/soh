#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: health_check

:Synopsis:

:Author:
    servilla

:Created:
    3/16/18
"""
import asyncio
from datetime import datetime, tzinfo
import logging
import os
import pickle
import re
import sys
from typing import List

import click
import daiquiri
import pendulum

from soh.config import Config
from soh.lock import Lock
from soh import mimemail
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


new_status = dict()


async def check_read_only(hosts):
    for host in hosts:
        await do_read_only(host)


async def do_read_only(host):
    st = datetime.now()
    host_ro = await server.read_only(host=host)
    logger.warning(f"Run time read only {host}: {datetime.now() - st}")
    if host_ro:
        new_status[host][0] = new_status[host][0] | Config.assertions["READ_ONLY"]


async def check_uptimes(hosts):
    for host in hosts:
        await do_uptime(host)


async def do_uptime(host):
    st = datetime.now()
    host_uptime = await server.uptime(host=host)
    logger.warning(f"Run time for uptime {host}: {datetime.now() - st}")
    new_status[host][1] = host_uptime
    if host_uptime is not None:
        new_status[host][0] = new_status[host][0] | load_status(get_load(host_uptime))


async def check_hosts(hosts):
    for host in hosts:
        await do_check(host)


async def do_check(host=None):
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

    st = datetime.now()
    new_status[host][0] = await server.check_server()
    logger.warning(f"Run time for check {host}: {datetime.now() - st}")


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

    if status & Config.assertions["READ_ONLY"]:
        diagnostics += "FILESYSTEM READ ONLY\n"

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


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
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
            mimemail.send_mail(subject=subject, msg=msg)
        except Exception as e:
            logger.error(e)
        return 1
    else:
        lock.acquire()
        logger.info(f"Lock file {lock.lock_file} acquired")

    soh_db = SohDb()
    soh_db.connect_soh_db()

    st = datetime.now()
    now_utc = pendulum.now("UTC")
    new_status["timestamp"] = now_utc.isoformat()

    if len(hosts) == 0:
        msg = "No hosts specified"
        logger.warning(msg)
    else:
        for host in hosts:
            new_status[host] = [0, None]

        loop = asyncio.get_event_loop()
        task1 = loop.create_task(check_hosts(hosts))
        task2 = loop.create_task(check_uptimes(hosts))

        if Config.READ_ONLY:
            task3 = loop.create_task(check_read_only(hosts))
            tasks = asyncio.gather(task1, task2, task3)
        else:
            tasks = asyncio.gather(task1, task2)

        loop.run_until_complete(tasks)

        for host in hosts:
            if notify:
                if host not in old_status or old_status[host][0] != new_status[host][0]:
                    diagnostic = do_diagnostics(host, new_status[host][0], new_status[host][1], now_utc)
                    if "Is now OK" in diagnostic:
                        subject = f"Status change: {host} is nominal"
                    else:
                        subject = f"Status change: {host} is problematic"
                    logger.warning(diagnostic)
                    try:
                        mimemail.send_mail(subject=subject, msg=diagnostic)
                    except Exception as e:
                        logger.error(e)
            if not quiet:
                print(f"{host}: {new_status[host][0]} - {new_status[host][1]}")
        if not quiet:
            print(f"Total processing time: {datetime.now() - st}")
        if store:
            with open(Config.STATUS_FILE, "wb") as f:
                pickle.dump(new_status, f)
    lock.release()
    logger.info("Lock file {} released".format(lock.lock_file))

    sys.exit(0)


if __name__ == "__main__":
    main()
