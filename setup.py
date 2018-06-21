#!/usr/bin/env python3
from setuptools import setup

setup(
    name='aquachain-kv',
    version='0.1.1',
    description='Aquachain GUI wallet',
    author_email='aquachain@riseup.net',
    author='Aquachain Authors',
    test_suite='tests',
    scripts=['aquachain-kv'],
    packages = ['aquachainkv'],
    data_files = [('aquachainkv', ['aquachainkv/aquachain.kv', 'img/aquachain.png'])],
    include_package_data=True,
)
