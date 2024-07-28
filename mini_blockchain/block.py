from datetime import datetime


class Transaction:
    def __init__(self, sender: str, recipient: str, amount: int) -> None:
        self.sender = sender
        self.recipient = recipient
        self.amount = amount


class Block:
    def __init__(
        self,
        index: int,
        timestamp: datetime,
        transtacions: list[Transaction],
        proof: int,
        previous_hash: str,
    ) -> None:
        self.index: int = index
        self.timestamp: datetime = timestamp
        self.transactions: list[Transaction] = transtacions
        self.proof: int = proof
        self.previous_hash: str = previous_hash
