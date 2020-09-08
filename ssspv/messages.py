import struct
import random
import time

from .serialize import Serialize
from . import settings


def version():
    ''' Advertize version, this message is mandatory and must be the first message.

    The remote node will respond with its own version, additionally further communication
    will only be possible if the remote peer responds with a "verack".
    '''

    version = settings.VERSION
    services = 1
    timestamp = int(time.time())
    source_address = b'\x00'*26
    destination_address = b'\x00'*26
    nonce = random.getrandbits(64)
    sub_version_num = b'\x00'
    start_height = 0

    payload = struct.pack(
        '<LQQ26s26sQsL',
        version,
        services,
        timestamp,
        source_address,
        destination_address,
        nonce,
        sub_version_num,
        start_height
    )

    return Serialize.wrap_network_message(b'version', payload)


def verack():
    ''' Sent in response to "version". Consists of a message header with the command string "verack". '''
    return Serialize.wrap_network_message(b'verack', b'')


def get_blocks(hash_count, hash_stop, block_locator_hashes=settings.GENESIS_BLOCK):
    ''' Describes a bitcoin transaction, usually sent in reply to "getdata". '''

    version = settings.VERSION

    payload = struct.pack('<LB32s32s', version, hash_count, block_locator_hashes, hash_stop)
    return Serialize.wrap_network_message(b'getblocks', payload)


def get_headers(hash_count, hash_stop, block_locator_hashes=settings.GENESIS_BLOCK):
    ''' Returns a "headers" packet containing the headers of blocks from the last known hash up
    to hash_stop or 2000 blocks, whichever comes first. '''

    version = settings.VERSION

    payload = struct.pack('<LB32s32s', version, hash_count, block_locator_hashes, hash_stop)
    return Serialize.wrap_network_message(b'getheaders', payload)


def tx(tx_in, tx_out):
    ''' Return an inv packet containing the list of blocks starting right after the last known hash in
    the block locator object, up to hash_stop or 500 blocks, whichever comes first. '''

    version = 1
    flag = 1
    locktime = 0

    payload = struct.pack('<LBsBsL', version, flag, tx_in, tx_out, locktime)

    return Serialize.wrap_network_message(b'tx', payload)
