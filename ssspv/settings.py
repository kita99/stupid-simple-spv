import logging
import binascii

HEXDUMP = True
VERSION = 31800
GENESIS_BLOCK = binascii.unhexlify('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')

MAGIC_BYTES = {
    'mainnet': b'\xe3\xe1\xf3\xe8',
    'testnet3': b'\xf4\xe5\xf3\xf4',
    'regtest': b'\xda\xb5\xbf\xfa',
}



logging.basicConfig(level=logging.DEBUG)
