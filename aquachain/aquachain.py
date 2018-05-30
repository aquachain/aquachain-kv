from web3 import Web3
from eth_account import Account
from ethereum import utils
import os
from eth_account.messages import defunct_hash_message
from mnemonic import Mnemonic
from aquachain.bip44 import HDPrivateKey
import logging

log = logging.Logger("AQUA", level=logging.DEBUG)

class AquaTool(object):
    def __init__(self, rpchost='', ipcpath=''):
        self.providers = []
        if ipcpath != '':
            log.info("using ipc: %s", ipcpath)
            self.providers.append(Web3.IPCProvider(os.path.expanduser(ipcpath)))

        if rpchost != '':
            log.info("using httprpc: %s", rpchost)
            self.providers.append(Web3.HTTPProvider(rpchost))

        if len(self.providers) == 0:
            raise Exception("need either ipc or http or both")

        self.w3 = Web3(self.providers)

    # Result returns the RPC response (or empty string), and logs any errors
    def Result(self, method, params):
        j = {}
        try: j = self.providers[0].make_request(method, params)
        except Exception:
            raise
        if 'error' in j:
            log.error("rpc responded with error: %s", j['error']['message'])
            return Exception(j['error']['message'])
        if 'result' in j:
            return j['result']
        raise Exception(f"unknown response kind: {j}")

    def setrpc(self, host):
        self.rpchost = host
        log.debug("new rpchost: %s", host)

    def getrpc(self):
        return self.rpchost

    def to_wei(self, amount, denom='ether'):
        return self.w3.toWei(amount, denom)

    def from_wei(self, amount, denom='ether'):
        return self.w3.fromWei(amount, denom)

    def to_hex(self, anything):
        return self.w3.toHex(anything)

    def from_hex(self, s):
        return self.w3.toAscii(s)

    def from_hex_i(self, i):
        return self.w3.toDecimal(i)
    #
    # key stuff

    def generate_key(self):
        return utils.sha3(os.urandom(4096))

    def generate_seed(self):
        return os.urandom(128 // 8)

    def generate_phrase(self):
        return self.seed_to_mnemonic(self.generate_seed())

    def private_to_public(self, private_key):
        raw_addr = utils.privtoaddr(private_key)
        pub_key = utils.checksum_encode(raw_addr)
        return pub_key

    def checksum_encode(self, raw_addr):
        return utils.checksum_encode(raw_addr)

    def seed_to_mnemonic(self, data):
        return Mnemonic('english').to_mnemonic(data)

    def seed_from_mnemonic(self, words, password=''):
        return Mnemonic('english').to_seed(words, password)

    def key_from_seed(self, seed):
        return HDPrivateKey.master_key_from_seed(seed)

    def key_from_mnemonic(self, words, password=''):
        return HDPrivateKey.master_key_from_mnemonic(words, password)

    def derive_hd(self, mkey, i):
        return HDPrivateKey.from_parent(mkey, i)

    def create_wallet(self, private_key, password=""):
        return self.w3.personal.importRawKey(self, private_key, password)

    def sign(self, private, data):
        message_hash = defunct_hash_message(text=data)
        signed_message = self.w3.eth.account.signHash(message_hash,
                                                 private_key=private)
        return signed_message

    def sign_tx(self, private, tx):
        signed = self.w3.eth.account.signTransaction(tx, private)
        log.debug("signed tx: %s", signed)
        return signed.rawTransaction

    def get_nonce(self, acct, fromblock):
        nonce = self.Result("aqua_getTransactionCount",
                              [self.checksum_encode(acct), fromblock])
        if nonce == '':
            log.error("empty nonce")
            return 0
        log.info("got tx nocne: %s", nonce)
        return int(nonce, 16)

    def send_raw_tx(self, rawtx):
        log.info("tryingf to send this tx: %s", rawtx)
        return self.Result("aqua_sendRawTransaction", [self.w3.toHex(rawtx)])

    def file_to_private(self, filename, password=''):
        with open(filename) as keyfile:
            keyfile_json = keyfile.read()
            return Account.decrypt(keyfile_json, password)
        return ''

    def private_to_account(self, private_key):
        return Account.privateKeyToAccount(private_key)

    # block stuff
    def gethead(self):
        log.debug("getting head block")
        return self.Result("aqua_getBlockByNumber",
                          ["latest", True])

    def gethead_header(self):
        log.debug("getting head header")
        return self.Result("aqua_getBlockByNumber",
                          ["latest", False])

    def getblock(self, number):
        log.debug("getting block %s", number)
        return self.Result("aqua_getBlockByNumber",
                          [str(hex(number)), True])

    def getblockbyhash(self, hash):
        log.info("getting block %s", hash)
        return self.Result("aqua_getBlockByHash", [hash, True])

    def getheader(self, number):
        log.debug("getting block %s", number)
        return self.Result("aqua_getBlockByNumber",
                          [str(hex(number)), False])

    def getheaderbyhash(self, hash):
        log.debug("getting block %s", hash)
        return self.Result("aqua_getBlockByHash", [hash, False])

    # tx
    #
    def gettransaction(self, hash):
        log.debug("getting tx %s", hash)
        return self.Result("aqua_getTransactionByHash", [hash])

    def sendtx(self, tx):
        log.debug("sending tx %s", tx)
        return self.Result("aqua_sendTransaction", [tx])

    # account
    #
    def getbalance(self, account, atblock='pending'):
        log.debug("getting balance %s", account)
        result = self.Result("aqua_balance", [account, atblock])
        if result is Exception:
            log.error("getbalance %s", result)
            return 0.00
        if result == '':
            return 0.00
        return float(result)

    def getaccounts(self):
        log.debug("getting accounts list")
        try :
            accounts = self.Result("aqua_accounts", [""])
            return accounts
        except Exception as e:
            log.error("error getting accounts: %s", e)
            return []
