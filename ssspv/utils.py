from hexdump import hexdump
import binascii
import hashlib

import base58

from . import settings


def shex(x):
    return binascii.hexlify(x).decode()


def b58checksum(x):
    checksum = hashlib.sha256(hashlib.sha256(x).digest()).digest()[:4]
    return base58.b58encode(x+checksum)


def sha256checksum(x):
    return hashlib.sha256(hashlib.sha256(x).digest()).digest()[:4]


def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d


def double_sha256(x):
    return hashlib.sha256(hashlib.sha256(x).digest()).digest()


def get_magic_bytes(network=False):
    if not network:
        network = settings.NETWORK

    if network in settings.MAGIC_BYTES:
        return int(binascii.hexlify(settings.MAGIC_BYTES[network][::-1]), 16)

    raise Exception(f'Invalid network "{network}", could not get magic bytes!')


def get_dns_seed(network=False):
    if not network:
        network = settings.NETWORK

    if network in settings.DNS_SEEDS:
        return settings.DNS_SEEDS[network]

    raise Exception('Invalid network "{netwokrk}" could not find DNS seed')


def dump_response(data, description):
    print(f'-------------- {description} ----------------')
    hexdump(data)
