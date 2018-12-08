from ..crypto import get_hash, verify
from ..model import Block, Transaction


class Verifier:
    def verify_transaction(self, transaction: Transaction) -> bool:
        """
        Step 1 : verify transaction
        """
        raise NotImplementedError

        return False

    def verify_block(self, block: Block) -> bool:
        """
        Step 2 : verify block
        """
        raise NotImplementedError

        return False
