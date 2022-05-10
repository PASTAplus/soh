#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: setup.py

:Synopsis:

:Author:
    servilla

:Created:
    3/16/18
"""
import setuptools

setuptools.setup(name='pastaplus.soh',
                 version='2022.05.07',
                 description='PASTA+ and related services State of Health monitoring',
                 author='PASTA+ project',
                 url='https://github.com/PASTAplus/soh',
                 license='Apache License, Version 2.0',
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 exclude_package_data={
                     '': ['settings.py, properties.py, config.py'],
                 }, )


def main():
    return 0


if __name__ == "__main__":
    main()
