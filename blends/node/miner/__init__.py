import threading

from .miner import Miner
from ..model import Block


class MinerThread(threading.Thread, Miner):
    def __init__(self, block: Block, mining: threading.Event):
        threading.Thread.__init__(self)
        self.miner = Miner(block, mining)

    def run(self):
        self.miner.mine()
