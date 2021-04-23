#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: sync

:Synopsis:

:Author:
    ide

:Created:
    1/28/2020
"""

import daiquiri
import pendulum
import requests
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

from soh.config import Config


logger = daiquiri.getLogger('sync.py: ' + __name__)

TRACE = False
GRACE_PERIOD = 2  # hours to allow GMN to catch up
ERROR = object()  # to provide a unique error indicator value


def get_recent_package_from_pasta_db(host=None, pasta_db_host=None):

    db = Config.DB_DRIVER + '://' + \
         Config.DB_USER + ':' + \
         Config.DB_PW + '@' + \
         pasta_db_host + '/' + \
         Config.DB_DB

    try:
        connection = create_engine(db)
    except Exception as e:
        logger.error(f'pasta DB connection failed: {db}')
        logger.error(e)
        return ERROR, ''

    past = pendulum.now(tz='US/Mountain').subtract(hours=GRACE_PERIOD)  # grace period to allow GMN to catch up

    is_edi = 'edirepository' in host
    if is_edi:
        scope = "and scope='edi'"
    else:
        scope = "and scope<>'edi'"

    query = ('select datapackagemanager.resource_registry.package_id, '
            'datapackagemanager.resource_registry.doi from '
            'datapackagemanager.resource_registry where date_created < '
            '\'TIME_IN_PAST\' '
            'SCOPE '
            'and resource_type=\'dataPackage\' '
            'order by date_created desc limit 1')
    query = query.replace('TIME_IN_PAST', past.to_iso8601_string()).replace('SCOPE', scope)
    if TRACE:
        print(query)

    try:
        result_set = connection.execute(query).fetchall()
        if result_set:
            package_id, doi = result_set[0]
            if TRACE:
                print(package_id, doi)
            return package_id, doi
        else:
            logger.error(f'pasta DB query failed to return a result: {query}')
            return ERROR, ''
    except Exception as e:
        logger.error(f'pasta DB query failed: {query}')
        logger.error(e)
        return ERROR, ''


def get_objects_from_pasta(pasta_host=None, pid=None):
    url = f"https://{pasta_host}/package/eml/{pid.replace('.', '/')}"
    if TRACE:
        print(f'get_objects_from_pasta\n   {url}')
    try:
        r = requests.get(url)
        if r:
            return(r.text.strip().split('\n'))
        else:
            logger.error(f'status={r.status_code} url={url}')
    except Exception as e:
        logger.error(e)
    return ERROR


def get_system_metadata(host=None, pasta_id=None):
    url = f"https://{host}/mn/v2/meta/{quote_plus(pasta_id)}"
    if TRACE:
        print(f'get_system_metadata\n   {url}')
    ok = False
    try:
        r = requests.get(url)
        if r:
            ok = True
        else:
            logger.error(f'status={r.status_code} url={url}')
        if TRACE:
            if not r:
                print(f'   status={r.status_code}')
    except Exception as e:
        logger.error(e)
    return ok


def get_ORE(host=None, doi=None):
    url = f"https://{host}/mn/v2/object/{doi}"
    if TRACE:
        print(f'get_ORE\n   {url}')
    ok = False
    try:
        r = requests.get(url)
        if r:
            ok = True
        else:
            logger.error(f'status={r.status_code} url={url}')
    except Exception as e:
        logger.error(e)
    return ok


async def is_down(host=None):
    IS_DOWN = True
    IS_UP = False

    if TRACE:
        print(f'\n{host}')

    pasta_host = Config.gmn_pasta_mapping[host]
    pasta_db_host = Config.gmn_pasta_db_host_mapping[host]

    recent_package, doi = get_recent_package_from_pasta_db(host, pasta_db_host)
    if recent_package != ERROR:
        if doi:
            if not get_ORE(host, doi):
                return IS_DOWN
        else:
            logger.error(f'DOI not found for {recent_package}')
            return IS_DOWN

        pids = get_objects_from_pasta(pasta_host, recent_package)
        if pids != ERROR:
            for pid in pids[:-1]:
                if not get_system_metadata(host, pid):
                    return IS_DOWN
            return IS_UP
    
    return IS_DOWN
