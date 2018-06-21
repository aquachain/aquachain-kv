#!/usr/bin/env python3
'''
Aquachain-KV Test Suite
'''

import unittest, os

class Test_AAA(unittest.TestCase):
    def test_foo(self):
        self.assertTrue(True)
    def test_imports(self):
        from aquachain.aquatool import AquaTool
        from aquachain.aquakeys import Keystore
        aqua = AquaTool(rpchost='https://c.onical.org', ipcpath=os.path.expanduser('~/.aquachain/aquachain.ipc'))

if __name__ == '__main__':
    unittest.main()
