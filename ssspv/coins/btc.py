class BTC:
    PRETTY_NAME                 = 'Bitcoin'

    NETWORK_MAGIC_BYTES         = bytes([0xE3, 0xE1, 0xF3, 0xE8])
    NETWORK_MAGIC_INT           = 3908297187

    MAX_BLOCK_SIZE              = 1000000

    DEFAULT_PORT                = 8333

    DNS_SEEDS = [
        'seed.bitcoinabc.org'
    ]

    GENESIS_BLOCK_HASH = '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'

    def __repr__(self):
        return repr(self.PRETTY_NAME)
