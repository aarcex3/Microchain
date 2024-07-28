from mini_blockchain.block import Block, Transaction


class Blockchain:
    def __init__(self) -> None:
        self.chain: list[Block] = []
        self.current_transactions: list[Transaction] = []

    def new_block(self):
        pass

    def new_transaction(self):
        pass

    @staticmethod
    def hash(block):
        pass

    @property
    def last_block(self):
        pass
