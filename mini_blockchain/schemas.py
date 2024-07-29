from pydantic import BaseModel, HttpUrl

from mini_blockchain.node import Node


class NewTransaction(BaseModel):
    sender: str
    recipient: str
    amount: int


class NewNodes(BaseModel):
    nodes: list[HttpUrl]
