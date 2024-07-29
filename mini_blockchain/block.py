import json
from datetime import datetime
from typing import Optional


class Transaction:
    def __init__(self, sender: str, recipient: str, amount: int) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_dict(self) -> dict:
        """
        Convert the Transaction to a dictionary.
        """
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
        }


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
