import json
import threading

from .. import DIFFICULTY
from .accountmanager import AccountManager
from .blockchain import Blockchain
from .miner import MinerThread
from .model import Block
from .networkmanager import NetworkManager
from .parser import Parser
from .util import now


class Node:
    def __init__(self,
                 broadcast_url: str,
                 key_path: str,
                 db_connection_string: str,
                 difficulty: int = DIFFICULTY):

        self.network_manager = NetworkManager(broadcast_url)
        self.account_manager = AccountManager(key_path)
        self.parser = Parser()
        self.blockchain = Blockchain(db_connection_string, difficulty)
        self.mining = None
        self.difficulty = difficulty
        self.update_blockchain()

        self.height = 0
        self.block = None

    def update_blockchain(self):
        fetched_data = self.network_manager.fetch_blocks()
        raise NotImplementedError

    def install_new_block(self):
        parent_block = self.blockchain.get_current()
        self.height = parent_block + 1
        self.block = Block.new_block(parent_block.hash, now(),
                                     self.account_manager.get_public_key(),
                                     self.difficulty)

    def new_block_arrived(self, block_json: str):

        block = self.parser.parse_block(block_json)
        if block:
            self.blockchain.append(block)
            new_block = self.blockchain.get_current()

            new_height = self.blockchain.dbmanager.get_height(new_block.hash)
            if not new_height:
                raise Exception(
                    "Fatal Error: get_height for inserted block failed")
            if new_height > self.height:
                if self.mining and self.mining.isSet():
                    self.stop_miner()
                    self.install_new_block()
                    self.start_miner()
                else:
                    self.install_new_block()
            else:
                print("New block arrived, but dismissed : parse error")

        else:
            print("New block arrived, but dismissed : parse error")

    def new_tx_arrived(self, tx_json: str):
        if not self.mining or not self.mining.isSet():
            print("New transaction arrived, but dismissed: not mining now")
            return

        tx = self.parser.parse_transaction(tx_json)
        if tx:
            if not self.blockchain.verifier.verify_transaction(tx):
                print(
                    "New transaction arrived, but dismissed: verification error"
                )
                return
            if not self.blockchain.validate_transaction(tx, self.block):
                print(
                    "New transaction arrived, but dismissed: validation error")
                return

            self.stop_miner()
            self.block.txs.append(tx)
            self.start_miner()

        else:
            print("New transaction arrived, but dismissed: parse error")

    def new_block_mint(self, block_json: str):
        if not self.mining or not self.mining.isSet():
            raise Exception("Unexpected mint")

        block = self.parser.parse_block(block_json)

        if block:
            if not self.blockchain.verifier.verify_block(block):
                raise Exception("New block mint, but verification failed")
            if not self.blockchain.validate_block(block):
                raise Exception("New block mint, but validation failed")
            self.blockchain.append(block)
            self.network_manager.new_block(block_json)
            self.stop_miner()
            self.install_new_block()
            self.start_miner()

        else:
            raise Exception("New block mint, but parse failed")

    def cmd_get_internal_balance(self):
        balance = self.blockchain.get_balance()
        res = {
            "balance": balance,
        }

        return json.dumps(res), 200

    def cmd_start_mining(self):
        if self.mining is None:
            self.start_miner()
            res = None
            status_code = 200
        elif self.mining.isSet():
            res = {'msg': 'miner is already running.'}
            status_code = 403
        else:
            self.mining.set()
            res = None
            status_code = 200
        return json.dumps(res), status_code

    def cmd_stop_mining(self):
        if self.mining is None:
            res = {'msg': 'miner is already stopped.'}
            status_code = 403

        elif self.mining.isSet():
            self.stop_miner()
            res = None
            status_code = 200
        else:
            res = {'msg': 'miner is already stopped.'}
            status_code = 403
        return json.dumps(res), status_code

    def stop_miner(self):
        self.mining.clear()
        self.mining = None
        self.miner = None

    def start_miner(self):
        mining = threading.Event()
        self.mining = mining
        self.mining.set()
        miner = MinerThread(self.block, mining)
        miner.start()
