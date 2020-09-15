import threading
import random
import socket
import time

import dataset

from . import utils


class Manager(threading.Thread):
    ''' Manage network and peers.  '''

    def __init__(self, ssspv=None):
        threading.Thread.__init__(self)

        self.log_level = ssspv.log_level
        self.log = utils.create_logger(self.log_level, 'NETWORK MANAGER')
        self.log.info('Initializing')

        self.ssspv = ssspv
        self.peers = {}
        self.database = dataset.connect('sqlite:///data/network', engine_kwargs={'connect_args': {'check_same_thread': False}})
        self.peer_addresses = self.load_known_peer_addresses()
        self.DESIRED_PEER_AMOUNT = 2

        self.network = Network(self)

    def load_known_peer_addresses(self):
        coin_name = self.ssspv.coin.PRETTY_NAME.lower()

        return self.database[f'{coin_name}_peer_addresses']

    def shutdown(self):
        self.log.info('Shutting down')

        if self.peers:
            for _, peer in self.peers.items():
                peer.shutdown()

        self.running = False

    def cleanup(self):
        self.database.close()

    def shutdown_dead_peers(self):
        pass

    def join(self, *args, **kwargs):
        if self.peers:
            for _, peer in self.peers.items():
                peer.join(*args, **kwargs)

        threading.Thread.join(self, *args, **kwargs)

    def start(self):
        self.running = False

        threading.Thread.start(self)

        while not self.running:
            pass

    def check_for_incoming_connections(self):
        pass

    def tick(self):
        self.log.info('Tick')

        self.check_for_incoming_connections()
        self.shutdown_dead_peers()

        if self.network.peers_are_behind_desired_amount():
            peer_address = self.network.pick_healthy_peer_address()

            if not peer_address:
                return

            self.network.spawn_peer(peer_address)

    def run(self):
        self.running = True

        while self.running:
            try:
                self.tick()
            except Exception as e:
                self.log.warning(e)
                self.log.warning('Bad bad not good')

            time.sleep(1)

        self.cleanup()
        self.log.info('Stopped')


class Network:
    def __init__(self, manager):
        self.log_level = manager.log_level
        self.log = utils.create_logger(self.log_level, 'NETWORK')
        self.log.info('Initializing')

        self.manager = manager
        self.active_peers = 0

    def peers_are_behind_desired_amount(self):
        if len(self.manager.peers) >= self.manager.DESIRED_PEER_AMOUNT:
            return False

        return True

    def get_active_peer_addresses(self):
        return self.manager.peers.keys()

    def discover_new_peer_addresses(self, index=0):
        dns_seed = self.manager.ssspv.coin.DNS_SEEDS[index]
        found_count = False

        self.log.info(f'Attempting to discover new peer addresses using "{dns_seed}"')
        peers = socket.gethostbyname_ex(dns_seed)[2]

        for address in peers:
            if self.manager.peer_addresses.find_one(address=address):
                # Peer address already exists
                continue

            self.manager.peer_addresses.insert(dict(
                address=address,
                health='unknown',
                last_used=None
            ))

            found_count += 1

        if found_count > 0:
            self.log.debug(f'Found {found_count} new peer addresses')
            return True

        if index < len(self.manager.ssspv.coin.DNS_SEEDS) - 1:
            self.log.warning(f'Peer address discovery using "{dns_seed}" was unsuccessful')
            return self.discover_new_peer_addresses(index + 1)

        self.log.critical('Cant find enough peers to meet goal, consider updating the DNS seed list')
        self.manager.shutdown()

        return False

    def pick_healthy_peer_address(self):
        health = False

        if self.manager.peer_addresses.count(health='unknown') > 0:
            health = 'unknown'

        if self.manager.peer_addresses.count(health='good') > 0:
            health = 'good'

        if not health:
            if self.discover_new_peer_addresses():
                return self.pick_healthy_peer_address()

            return False

        coin_name = self.manager.ssspv.coin.PRETTY_NAME.lower()
        active_peer_addresses = self.get_active_peer_addresses()

        query = utils.build_active_peer_exclusion_query(coin_name, health, active_peer_addresses)
        prospects = self.manager.database.query(query)
        address = random.choices(list(prospects))[0].get('address')

        self.log.debug(f'Peer {address} is joining the pool')
        return address

    def spawn_peer(self, peer_address):
        if not self.peers_are_behind_desired_amount():
            return

        socket = 'IMPLEMENT_ME'

        self.manager.peers[peer_address] = Peer(self, socket, peer_address)
        self.manager.peers[peer_address].start()


class Peer(threading.Thread):
    def __init__(self, network, socket, address):
        threading.Thread.__init__(self)

        self.log_level = network.log_level
        self.log = utils.create_logger(self.log_level, f'PEER ({address})')
        self.log.info('Initializing')

        self.network = network
        self.socket = socket
        self.address = address

    def shutdown(self):
        self.running = False
        self.log.info('Shutting down')

    def start(self):
        self.running = False
        threading.Thread.start(self)

        while not self.running:
            pass

    def tick(self):
        self.log.info('Tick')

    def run(self):
        self.running = True

        while self.running:
            try:
                self.tick()
            except:
                self.log.warning('Bad bad not good')
                pass

            time.sleep(1)

        self.log.info('Stopped')
