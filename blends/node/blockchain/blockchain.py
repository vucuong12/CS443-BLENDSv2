from typing import Dict

from ... import DIFFICULTY, GENESIS_HASH, REWARD
from ..model import Block, Transaction
from .dbmanager import DBManager
from .verifier import Verifier


class Blockchain:
    def __init__(self, db_connection_string: str,
                 difficulty: int = DIFFICULTY):

        self.verifier = Verifier()
        self.dbmanager = DBManager(db_connection_string)

    def append(self, block: Block) -> bool:
        if self.verifier.verify_block(block) and self.validate_block(block):
            self.dbmanager.insert_block(block)
            return True
        else:
            return False

    def validate_transaction(self, tx: Transaction, block: Block) -> bool:
        raise NotImplementedError
        return None

    def validate_block(self, block: Block) -> bool:
        """
        check difficulty
        """
        raise NotImplementedError
        return None

    def get_balance(self) -> Dict[str, int]:
        block = self.dbmanager.get_current()
        balance = self.dbmanager.get_block_balance(block.hash)
        return balance

    def get_current(self):
        return self.dbmanager.get_current()
