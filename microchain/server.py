from typing import Any
from uuid import uuid4

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from microchain.block import Block, Transaction
from microchain.blockchain import Blockchain
from microchain.node import Node
from microchain.schemas import NewNodes, NewTransaction

server: FastAPI = FastAPI()

node_identifier: str = str(uuid4()).replace("-", "")

blockchain: Blockchain = Blockchain()


@server.get("/mine")
def mine() -> JSONResponse:
    last_block: Block = blockchain.last_block
    last_proof: int = last_block.proof
    proof: int = blockchain.proof_of_work(last_proof=last_proof)
    new_transaction: Transaction = Transaction(
        sender="0", recipient=node_identifier, amount=1
    )
    blockchain.new_transaction(new_transaction)
    previous_hash: str = blockchain.hash(last_block)
    block: Block = blockchain.new_block(proof, previous_hash)
    response: dict[str, Any] = {
        "message": "New Block Forged",
        "index": block.index,
        "transactions": [transaction.to_dict() for transaction in block.transactions],
        "proof": block.proof,
        "previous_hash": block.previous_hash,
    }
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@server.post("/transactions/new")
def new_transaction(transaction: NewTransaction) -> JSONResponse:
    index: int = blockchain.new_transaction(
        transaction=Transaction(**transaction.model_dump())
    )
    response: dict[str, str] = {
        "message": f"Transaction will be added to Block {index}"
    }
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@server.get("/chain")
def full_chain() -> JSONResponse:
    response: dict[str, Any] = {
        "chain": [block.to_dict() for block in blockchain.chain],
        "length": len(blockchain.chain),
    }
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@server.post("/nodes/register")
def register_nodes(new_nodes: NewNodes) -> JSONResponse:
    for node_url in new_nodes.nodes:
        node = Node(address=str(node_url))
        blockchain.register_node(node=node)

    response: dict[str, Any] = {
        "message": "New nodes have been added",
        "total_nodes": list(blockchain.nodes),
    }
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@server.get("/nodes/resolve")
def consensus() -> JSONResponse:
    replaced: bool = blockchain.resolve_conflicts()

    if replaced:
        response: dict[str, Any] = {
            "message": "Our chain was replaced",
            "new_chain": blockchain.chain,
        }
    else:
        response: dict[str, Any] = {
            "message": "Our chain is authoritative",
            "chain": blockchain.chain,
        }

    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(server, host="0.0.0.0", port=5000)
