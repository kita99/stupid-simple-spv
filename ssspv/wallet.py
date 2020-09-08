from collections import namedtuple
import hashlib
import random
import os

import ecdsa

from .utils import shex
import utils


Wallet = namedtuple('Wallet', ['private_key', 'WIF', 'public_key', 'public_address'])


def generate_private_key(seed, hex_string=False):
    random.seed(seed)
    private_key = bytes([random.randint(0, 255) for x in range(32)])
    WIF = utils.b58checksum(b'\x80' + private_key)

    return private_key, WIF


def derive_public_key(private_key, hex_string=False):
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key = b'\x04' + vk.to_string()

    return public_key


def derive_public_address(public_key):
    hash160 = utils.ripemd160(hashlib.sha256(public_key).digest()).digest()
    public_address = utils.b58checksum(b'\x00' + hash160)
    return public_address


def create_new(seed=False, bytes=False):
    if not seed:
        seed = os.urandom(128)

    private_key, WIF = generate_private_key(seed)
    public_key = derive_public_key(private_key)
    public_address = derive_public_address(public_key)

    if bytes:
        return Wallet(
            private_key=private_key,
            WIF=WIF,
            public_key=public_key,
            public_address=public_address
        )

    return Wallet(
        private_key=shex(private_key),
        WIF=WIF.decode(),
        public_key=shex(public_key),
        public_address=public_address.decode()
    )
