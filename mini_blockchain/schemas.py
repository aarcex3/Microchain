from pydantic import BaseModel


class NewTransaction(BaseModel):
    sender: str
    recipient: str
    amount: int
