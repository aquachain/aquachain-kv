#!/usr/bin/env python3
from setuptools import setup

setup(
    name='aquachain-kv',
    version='0.0.1',
    description='Aquachain GUI wallet',
    url='https://github.com/aquachain/aquachain-kv',
    long_description='Aquachain GUI wallet, using kivy, kivymd, and python 3.6.5',
    author='Aquachain Authors',
    author_email='aquachain@riseup.net',
    scripts=['aquachain-kv'],
    packages = ['aquachainkv'],
    data_files = [('aquachainkv', ['aquachainkv/aquachain.kv', 'img/aquachain.png'])],
    include_package_data=True,
    install_requires = ['aquachain.py', 'kivy', 'kivymd'],
    dependency_links = ['https://github.com/aquachain/aquachain.py/tarball/master#egg=aquachain.py',
    'https://github.com/kivy/kivy/tarball/master#egg=kivy',
    'https://gitlab.com/kivymd/KivyMD/-/archive/master/KivyMD-master.tar.gz#egg=kivymd'],
    license = 'GPL',
    test_suite='tests',
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'License :: Free for non-commercial use',
        'License :: OSI Approved :: GNU General Public License (GPL)',
	],
)
