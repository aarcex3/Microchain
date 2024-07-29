import hashlib
import json
from datetime import datetime
from typing import List

from mini_blockchain.block import Block, Transaction


class Blockchain:
    def __init__(self) -> None:
        """
        Initialize the Blockchain with an empty chain and a list for current transactions.
        Create the genesis block and append it to the chain.
        """
        self.chain: List[Block] = []
        self.current_transactions: List[Transaction] = []
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """
        Create the genesis block and append it to the blockchain.

        The genesis block is the first block in the blockchain with:
        - An index of 0
        - A predefined proof of work
        - A previous_hash of "0"
        """
        genesis_block = Block(
            index=0,
            timestamp=datetime.now(),
            transactions=[Transaction("0", "0", 0)],  # Example transaction
            proof=0,
            previous_hash="0",
        )
        self.chain.append(genesis_block)

    def new_block(self, proof: int, previous_hash: str) -> Block:
        """
        Create a new block and add it to the blockchain.

        Args:
            proof (int): The proof of work for the new block.
            previous_hash (str): The hash of the previous block.

        Returns:
            Block: The newly created Block.
        """
        block = Block(
            index=len(self.chain),
            timestamp=datetime.now(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or self.hash(self.chain[-1]),
        )
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, transaction: Transaction) -> int:
        """
        Add a new transaction to the list of transactions for the next block.

        Args:
            transaction (Transaction): The transaction to be added.

        Returns:
            int: The index of the block that will hold this transaction.
        """
        self.current_transactions.append(transaction)
        return self.last_block.index + 1

    @staticmethod
    def hash(block: Block) -> str:
        """
        Creates a SHA-256 hash of a Block.

        Args:
            block (Block): The block to be hashed.

        Returns:
            str: The SHA-256 hash of the block.
        """
        # Convert the block to a dictionary
        block_dict = block.to_dict()

        # Make sure the dictionary is ordered by keys for consistent hashing
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self) -> Block:
        """
        Return the last Block in the chain.

        Returns:
            Block: The most recent block in the blockchain.
        """
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
        """
        Simple Proof of Work Algorithm:
            - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
            - p is the previous proof, and p' is the new proof
        Args:
            last_proof (int)
        Return:
            proff (int)
        """
        proof: int = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        Args:
            last_proof (int): Previous Proof
            proof (int): Current Proof

        Return:
            (bool): True if correct, False if not.
        """
        guess: bytes = f"{last_proof}{proof}".encode()
        guess_hash: str = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
