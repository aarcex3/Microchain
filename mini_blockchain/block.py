import json
from datetime import datetime

from mini_blockchain.transaction import Transaction


class Block:
    def __init__(
        self,
        index: int,
        timestamp: datetime,
        transactions: list[Transaction],
        proof: int,
        previous_hash: str,
    ) -> None:
        self.index: int = index
        self.timestamp: datetime = timestamp
        self.transactions: list[Transaction] = transactions
        self.proof: int = proof
        self.previous_hash: str = previous_hash

    def to_dict(self) -> dict:
        """
        Convert the Block to a dictionary.
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp.isoformat(),
            "transactions": [tx.to_dict() for tx in self.transactions],
            "proof": self.proof,
            "previous_hash": self.previous_hash,
        }
