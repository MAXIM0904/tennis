from pydantic import BaseModel


class SchemaInventory(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
