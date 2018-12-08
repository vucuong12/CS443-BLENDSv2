import collections
from typing import Dict, List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ... import GENESIS_HASH, REWARD
from ..model import Block, Transaction


class DBManager:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = None

    def get_session(self):
        if not self.session:
            self.session = self.sessionmaker()
        return self.session

    def search_block(self, block_hash: str) -> Optional[Block]:
        """
        Step 1
        """
        session = self.get_session()
        for block in session.query(Block).all():
            print(block)

        raise NotImplementedError

        return None

    def get_height(self, block_hash: str) -> Optional[int]:
        """
        Step 2
        """
        session = self.get_session()
        for block in session.query(Block).all():
            print(block)

        raise NotImplementedError

        return None

    def get_current(self) -> Block:
        """
        Step 3
        """
        session = self.get_session()
        for block in session.query(Block).all():
            print(block)

        raise NotImplementedError
        return

    def get_longest(self) -> List[Block]:
        """
        Step 4
        """
        session = self.get_session()
        for block in session.query(Block).all():
            print(block)

        raise NotImplementedError
        return

    def search_transaction(self, tx_hash: str) -> Optional[Transaction]:
        """
        Step 5
        """
        session = self.get_session()
        for tx in session.query(Transaction).all():
            print(tx)

        raise NotImplementedError

        return None

    def get_block_balance(self, block_hash: str) -> Dict[str, int]:
        """
        Step 6
        """
        block = self.search_block(block_hash)
        print(block)

        raise NotImplementedError
        return None

    def insert_block(self, block: Block) -> bool:
        session = self.get_session()
        session.add(block)
        session.commit()

        return True
