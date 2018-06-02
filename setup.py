#!/usr/bin/env python3
from setuptools import setup

setup(
    name='aquachain-kv',
    version='0.1.1',
    description='Aquachain GUI wallet',
    author='Satoshi Nakamoto',
    test_suite='tests',
    scripts=['aquachain-kv'],
    packages = ['aquachain'],
    data_files = [('aquachain', ['aquachain/aquachain.kv', 'img/aquachain.png'])],
    include_package_data=True,
)
