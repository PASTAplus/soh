#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: server

:Synopsis:

:Author:
    servilla

:Created:
    3/16/18
"""
import daiquiri

from soh.config import Config
from soh.asserts import apache
from soh.asserts import audit
from soh.asserts import auth
from soh.asserts import gmn
from soh.asserts import jetty
from soh.asserts import ldap
from soh.asserts import package
from soh.asserts import portal
from soh.asserts import server
from soh.asserts import solr
from soh.asserts import sync
from soh.asserts import tomcat

logger = daiquiri.getLogger('server.py: ' + __name__)


class Server(object):
    
    def __init__(self, host=None):
        self._host = host

    async def check_server(self):
        status = Config.UP
        if await self._server_is_down():
            status = status | Config.assertions['SERVER_DOWN']
        return status

    async def _server_is_down(self):
        server_is_down = False
        server_uptime = await server.uptime(host=self._host)
        if server_uptime is None:
            server_is_down = True
        return server_is_down


class JettyServer(Server):
    """
    The JettyServer uniquely identifies services provided by the PASTA
    Gatekeeper service as identified by the host name "pasta".
    """

    async def check_server(self):
        status = Config.UP
        if await self._jetty_is_down():
            status = status | Config.assertions['JETTY_DOWN']
            if await self._server_is_down():
                status = status | Config.assertions['SERVER_DOWN']
        return status

    async def _jetty_is_down(self):
        return await jetty.is_down(host=self._host)


class TomcatServer(Server):
    """
    The TomcatServer identifies services provided by the workhorse PASTA
    services, such as the Data Package Manager and Audit Manager.
    """

    async def check_server(self):
        status = Config.UP
        if await self._tomcat_is_down():
            status = status | Config.assertions['TOMCAT_DOWN']
            if await self._server_is_down():
                status = status | Config.assertions['SERVER_DOWN']
        return status

    async def _tomcat_is_down(self):
        return await tomcat.is_down(host=self._host)


class SolrServer(Server):
    """
    The SolrServer identifies services provided by the PASTA search engine
    service, Solr.
    """

    async def check_server(self):
        status = Config.UP
        if await self._solr_is_down():
            status = status | Config.assertions['SOLR_DOWN']
            if await self._server_is_down():
                status = status | Config.assertions['SERVER_DOWN']
        return status

    async def _solr_is_down(self):
        return await solr.is_down(host=self._host)


class LdapServer(Server):
    """
    The LdapServer identifies services provided by the PASTA authentication
    service, LDAP.
    """

    async def check_server(self):
        status = Config.UP
        if await self._ldap_is_down():
            status = status | Config.assertions['LDAP_DOWN']
            if await self._server_is_down():
                status = status | Config.assertions['SERVER_DOWN']
        return status

    async def _ldap_is_down(self):
        return await ldap.is_down(host=self._host)


class ApacheServer(Server):
    """
    The ApacheServer identifies services provided by the Apache web server.
    """

    async def check_server(self):
        status = Config.UP
        if await self._apache_is_down():
            status = status | Config.assertions['APACHE_DOWN']
            if await self._server_is_down():
                status = status | Config.assertions['SERVER_DOWN']
        return status

    async def _apache_is_down(self):
        return await apache.is_down(host=self._host)


class ApacheTomcatServer(Server):
    """
    The ApacheTomcatServer identifies services provided by the PASTA data portal
    user interface.
    """

    async def check_server(self):
        status = Config.UP
        if await self._tomcat_is_down():
            status = status | Config.assertions['TOMCAT_DOWN']
            if await self._apache_is_down():
                status = status | Config.assertions['APACHE_DOWN']
                if await self._server_is_down():
                    status = status | Config.assertions['SERVER_DOWN']
        return status

    async def _apache_is_down(self):
        return await apache.is_down(host=self._host)

    async def _tomcat_is_down(self):
        return await tomcat.is_down(host=self._host)


class AuthServer(ApacheServer):
    """
    The AuthServer identifies services provided by the EDI Authentication
    Service.
    """
    async def check_server(self):
        status = Config.UP
        if await self._auth_is_down():
            status = status | Config.assertions['AUTH_DOWN']
            if await self._apache_is_down():
                status = status | Config.assertions['APACHE_DOWN']
                if await self._server_is_down():
                    status = status | Config.assertions['SERVER_DOWN']
        return status

    async def _auth_is_down(self):
        return await auth.is_down(host=self._host)


class GmnServer(Server):
    """
    The GmnServer identifies services provided by the DataONE Generic Member
    Node API.
    """

    async def check_server(self):
        status = Config.UP
        if await self._sync_is_down():
            status = status | Config.assertions['SYNC_DOWN']
            if await self._gmn_is_down():
                status = status | Config.assertions['GMN_DOWN']
                if await self._apache_is_down():
                    status = status | Config.assertions['APACHE_DOWN']
                    if await self._server_is_down():
                        status = status | Config.assertions['SERVER_DOWN']
        return status

    async def _apache_is_down(self):
        return await apache.is_down(host=self._host)

    async def _gmn_is_down(self):
        return await gmn.is_down(host=self._host)

    async def _sync_is_down(self):
        return await sync.is_down(host=self._host)


class PortalServer(ApacheTomcatServer):
    """
    The PortalServer identifies services provided by the communities data
    portal interface.
    """

    async def check_server(self):
        status = Config.UP
        if await self._portal_is_down():
            status = status | Config.assertions['PORTAL_DOWN']
            if await self._tomcat_is_down():
                status = status | Config.assertions['TOMCAT_DOWN']
            if await self._apache_is_down():
                status = status | Config.assertions['APACHE_DOWN']
                if await self._server_is_down():
                    status = status | Config.assertions['SERVER_DOWN']
        return status

    async def _portal_is_down(self):
        return await portal.is_down(host=self._host)


class PackageServer(TomcatServer):

     async def check_server(self):
         status = Config.UP
         if await self._package_is_down():
             status = status | Config.assertions['PACKAGE_DOWN']
             if await self._tomcat_is_down():
                 status = status | Config.assertions['TOMCAT_DOWN']
                 if await self._server_is_down():
                     status = status | Config.assertions['SERVER_DOWN']
         return status

     async def _package_is_down(self):
         return await package.is_down(host=self._host)


class AuditServer(TomcatServer):

     async def check_server(self):
         status = Config.UP
         if await self._audit_is_down():
             status = status | Config.assertions['AUDIT_DOWN']
             if await self._tomcat_is_down():
                 status = status | Config.assertions['TOMCAT_DOWN']
                 if await self._server_is_down():
                     status = status | Config.assertions['SERVER_DOWN']
         return status

     async def _audit_is_down(self):
         return await audit.is_down(host=self._host)