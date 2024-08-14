from pydantic import BaseModel

class Chat(BaseModel):
    id: int
    name: str
    price: float