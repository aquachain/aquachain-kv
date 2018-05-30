#!/usr/bin/env python3
import unittest
from aquachain.keystore import Keystore, HDPrivateKey
from aquachain.aquachain import AquaTool
import os
import logging

log = logging.Logger("AQUA", level=logging.DEBUG)

aqua = AquaTool(rpchost='http://localhost:8543', ipcpath=os.path.expanduser('~/.aquachain/aquachain.ipc'))


class Test_Keystore(unittest.TestCase):
    keystore = Keystore(directory='testdata')

    def test_asavekeys(self):
        for i in range(1):
            phrase = aqua.generate_phrase()
            filename = self.keystore.save_phrase(phrase)
            log.info("saved key %s", filename)

    def test_listphrases(self):
        log.info("listphrase test")
        keys = self.keystore.listphrases()
        self.assertFalse(len(keys) == 0)
        for key in keys:
            log.info("found phrase: %s", key)

    def test_loadkey(self):
        keys = self.keystore.listphrases()
        self.assertFalse(len(keys) == 0)
        for phrase in keys:
            log.info("[loader] %s", phrase)
            key = aqua.key_from_mnemonic(phrase, 'password')
            log.info("[loaded] %s %s",
                     key.public_key.address(), key._key.to_hex())


    def test_loadphrase(self):
        phrase = 'drum legend crowd awesome ethics cat topic grid clerk equip display cross'
        mkey = self.keystore.load_phrase(phrase, "password")
        for i in range(10):
            key = HDPrivateKey.from_parent(mkey, i)
            log.info("HD%s: %s", i, key.public_key.address())

    def test_loadphrases(self):
        phrases = Keystore(directory='.').listphrases()
        keys = self.keystore.load_phrases(phrases, "password")
        self.assertFalse(len(keys) == 0)
        for key in keys:
            log.info("loadphrases: %s", key.public_key.address())

    def test_loadfile(self):
        return
        key_filename = os.path.join('testdata',
                                    'aqua1527314056152731405672612.wallet')
        password = 'password'
        phrase = self.keystore.readfile(key_filename)
        hdkey = self.keystore.load_phrase(phrase['poem'], password)
        pub = hdkey.public_key.address()
        log.info('Found master key: %s', pub)

        # 44/0/0
        # self.assertEqual('0x99e4c027d183aa37684a558b5804cce730456a63', pub)

        # 44/0/0/0
        self.assertEqual('0x7e362eef9425dae8b84374543c78d539869b6e3a', pub)


    def test_zd_wallets(self):
        phrases = self.keystore.listphrases()
        keys = self.keystore.load_phrases([phrases[0]], "password")
        self.assertFalse(len(keys) == 0)
        key = keys[0]
        log.info("hdwallet: %s", phrases[0])
        oldkey = ''
        for i in range(100):
            pub = key.public_key.address()
            log.info("test_hd_wallets: %s (%s)", pub, key._key.to_hex())
            key = self.keystore.from_parent_key(key, i)
            self.assertNotEqual(oldkey, key)
            oldkey = key

    def test_keystoredir(self):
        keys = self.keystore.listphrases()
        self.assertTrue(len(keys) != 0)
        ks1 = Keystore(directory='testdata2')
        keys1 = ks1.listphrases()
        self.assertTrue(len(keys1) == 0)



if __name__ == '__main__':
    unittest.main()
