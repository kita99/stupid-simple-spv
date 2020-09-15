import signal

from .utils import get_log_level_object
from .utils import create_logger
from .coins import Coin
from . import network



class SSSPV():
    def __init__(self, app, coin, log_level='warning'):
        signal.signal(signal.SIGINT, self.signal_handler)

        self.app = app
        self.coin = Coin(coin)
        self.log_level = get_log_level_object(log_level)
        self.log = create_logger(self.log_level, 'SSSPV')

        self.network_manager = network.Manager(self)
        self.network_manager.start()

    def signal_handler(self, sig, frame):
        self.log.info('Termination signal received')
        self.stop()

    def stop(self):
        self.log.info('Shutting down')
        if self.network_manager:
            self.network_manager.shutdown()
