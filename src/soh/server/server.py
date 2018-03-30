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
from soh.asserts import jetty
from soh.asserts import ldap
from soh.asserts import server
from soh.asserts import solr
from soh.asserts import tomcat

logger = daiquiri.getLogger('server.py: ' + __name__)


class Server(object):

    @staticmethod
    def check_server(host=None):
        status = Config.UP
        if Server.server_is_down(host=host):
            status = status | Config.assertions['SERVER_DOWN']
        return status

    @staticmethod
    def server_is_down(host=None):
        server_is_down = False
        server_uptime = server.uptime(host=host, user=Config.USER,
                                      key_path=Config.KEY_PATH,
                                      key_pass=Config.KEY_PASS)
        if server_uptime is None:
            server_is_down = True
        return server_is_down


class JettyServer(Server):
    """
    The JettyServer uniquely identifies services provided by the PASTA
    Gatekeeper service as identified by the host name "pasta".
    """

    @staticmethod
    def check_server(host=None):
        status = Config.UP
        if JettyServer.jetty_is_down(host=host):
            status = status | Config.assertions['JETTY_DOWN']
            if JettyServer.server_is_down(host=host):
                status = status | Config.assertions['SERVER_DOWN']
        return status

    @staticmethod
    def jetty_is_down(host=None):
        return jetty.is_down(host=host)


class TomcatServer(Server):
    """
    The TomcatServer identifies services provided by the workhorse PASTA
    services, such as the Data Package Manager and Audit Manager.
    """

    @staticmethod
    def check_server(host=None):
        status = Config.UP
        if TomcatServer.tomcat_is_down(host=host):
            status = status | Config.assertions['TOMCAT_DOWN']
            if TomcatServer.server_is_down(host=host):
                status = status | Config.assertions['SERVER_DOWN']
        return status

    @staticmethod
    def tomcat_is_down(host=None):
        return tomcat.is_down(host=host)


class SolrServer(Server):
    """
    The SolrServer identifies services provided by the PASTA search engine
    service, Solr.
    """

    @staticmethod
    def check_server(host=None):
        status = Config.UP
        if SolrServer.solr_is_down(host=host):
            status = status | Config.assertions['SOLR_DOWN']
            if SolrServer.server_is_down(host=host):
                status = status | Config.assertions['SERVER_DOWN']
        return status

    @staticmethod
    def solr_is_down(host=None):
        return solr.is_down(host=host)


class LdapServer(Server):
    """
    The LdapServer identifies services provided by the PASTA authentication
    service, LDAP.
    """

    @staticmethod
    def check_server(host=None):
        status = Config.UP
        if LdapServer.ldap_is_down(host=host):
            status = status | Config.assertions['LDAP_DOWN']
            if LdapServer.server_is_down(host=host):
                status = status | Config.assertions['SERVER_DOWN']
        return status

    @staticmethod
    def ldap_is_down(host=None):
        return ldap.is_down(host=host)
