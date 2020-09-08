import struct

from . import utils
from . import settings


class Serialize:
    @staticmethod
    def wrap_network_message(command, payload):
        message = struct.pack('<L12sL4s', utils.get_magic_bytes(), command, len(payload), utils.sha256checksum(payload)) + payload

        if settings.HEXDUMP:
            utils.dump_message(message, 'sent')

        return message

    @staticmethod
    def unwrap_network_message(coin, payload):
        pass
