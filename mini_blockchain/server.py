from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from mini_blockchain.block import Block, Transaction
from mini_blockchain.blockchain import Blockchain
from mini_blockchain.schemas import NewTransaction

server: FastAPI = FastAPI()

node_identifier: str = str(uuid4()).replace("-", "")

blockchain: Blockchain = Blockchain()


@server.get("/mine")
def mine():
    last_block: Block = blockchain.last_block
    last_proof: int = last_block.proof
    proof: int = blockchain.proof_of_work(last_proof=last_proof)
    new_transaction: Transaction = Transaction(
        sender="0", recipient=node_identifier, amount=1
    )
    blockchain.new_transaction(new_transaction)
    previous_hash: str = blockchain.hash(last_block)
    block: Block = blockchain.new_block(proof, previous_hash)
    response = {
        "message": "New Block Forged",
        "index": block.index,
        "transactions": [transaction.to_dict() for transaction in block.transactions],
        "proof": block.proof,
        "previous_hash": block.previous_hash,
    }
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@server.post("/transactions/new")
def new_transaction(transaction: NewTransaction):
    index: int = blockchain.new_transaction(transaction=transaction)
    response: dict = {"message": f"Transaction will be added to Block {index}"}
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@server.get("/chain")
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(server, host="0.0.0.0", port=5000)
