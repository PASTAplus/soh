#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Mod: test_async

:Synopsis:

:Author:
    servilla

:Created:
    4/22/21
"""
import asyncio
from datetime import datetime

import daiquiri
import pendulum
import pytest

from soh.config import Config
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


logger = daiquiri.getLogger(__name__)


def test_hosts():
    print()
    start_time = datetime.now()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_hosts())
    end_time = datetime.now()
    print(f"Testing done: {end_time - start_time} seconds")


async def check_hosts():
    hosts = (
        "pasta-d.lternet.edu",
        "pasta-s.lternet.edu",
        "pasta.lternet.edu",
        "portal-d.edirepository.org",
        "portal-s.edirepository.org",
        "portal.edirepository.org",
        "package-d.lternet.edu",
        "package-s.lternet.edu",
        "package.lternet.edu",
        "audit-d.lternet.edu",
        "audit-s.lternet.edu",
        "audit.lternet.edu",
        "gmn-s.lternet.edu",
        "gmn.lternet.edu",
        "gmn-s.edirepository.org",
        "gmn.edirepository.org",
        "solr-d.lternet.edu",
        "solr-s.lternet.edu",
        "solr.lternet.edu",
        "auth.edirepository.org",
        "ldap.edirepository.org",
        "unit.lternet.edu",
        "vocab.lternet.edu",
        "seo.edirepository.org",
        "tweeter.edirepository.org",
        "space.lternet.edu",
        "josh.lternet.edu",
        "ezeml.edirepository.org"
    )
    for host in hosts:
        await do_check(host)


async def do_check(host=None):
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

    status = await server.check_server()
    print(host, status)
