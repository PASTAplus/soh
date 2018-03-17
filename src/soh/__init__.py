#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: __init__

:Synopsis:

:Author:
    servilla

:Created:
    3/16/18
"""

import logging
import os

import daiquiri

cwd = os.path.dirname(os.path.realpath(__file__))
logfile = cwd + '/soh.log'
daiquiri.setup(level=logging.WARN,
               outputs=(daiquiri.output.File(logfile), 'stdout',))
logger = daiquiri.getLogger('__init__.py: ' + __name__)


def main():
    return 0


if __name__ == "__main__":
    main()
