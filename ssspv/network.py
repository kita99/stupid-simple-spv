import socket
import random
import struct

from hexdump import hexdump

from .settings import logging
from . import settings
from . import messages
from . import utils


def sock_read(sock, count):
    ret = b''

    while len(ret) < count:
        ret += sock.recv(count-len(ret))

    return ret


def read_message(sock):
    header = sock_read(sock, 24)
    magic, command, payload_length, checksum = struct.unpack('<L12sL4s', header)
    payload = sock_read(sock, payload_length)

    logging.info(f'Received command: {command}')

    assert utils.sha256checksum(payload) == checksum

    if settings.HEXDUMP:
        utils.dump_response(header, 'header')

        if payload:
            utils.dump_response(payload, 'header')

    return command, payload


def connect():
    peers = socket.gethostbyname_ex(utils.get_dns_seed())[2]
    peer = random.choice(peers)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((peer, 8333))
    logging.info(f'Connected to PEER: {peer}')

    # Send version
    sock.send(messages.version())
    # Get response
    command, payload = read_message(sock)
    command, payload = read_message(sock)

    # Acknowledge version
    sock.send(messages.verack())
    command, payload = read_message(sock)

    sock.send(messages.get_headers(hash_count=1, hash_stop=b'\x00'*32))
    command, payload = read_message(sock)
    command, payload = read_message(sock)

    # sock.send(messages.get_blocks(hash_count=1, hash_stop=b'\x00'*32))

    # command, payload = read_message(sock)
    # command, payload = read_message(sock)

    return sock
