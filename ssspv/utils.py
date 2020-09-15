import binascii
import hashlib
import logging

from hexdump import hexdump
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


def get_log_level_object(log_level):
    if log_level == 'debug':
        return logging.DEBUG

    if log_level == 'info':
        return logging.INFO

    if log_level == 'warning':
        return logging.WARNING

    if log_level == 'critical':
        return logging.CRITICAL

    raise Exception(f'Invalid log level {log_level}')


def create_logger(log_level, name=None):
    log_format = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s -> %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(log_format)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    logger.propagate = False
    logger.addHandler(ch)

    return logger
