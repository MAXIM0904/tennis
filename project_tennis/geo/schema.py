from pydantic import BaseModel
from typing import List


class SchemaCountry(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class SchemaCity(BaseModel):
    requests: List[SchemaCountry]

    class Config:
        orm_mode = True


class SchemaDistrict(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class SchemaListDistrict(BaseModel):
    requests: List[SchemaDistrict]

    class Config:
        orm_mode = True
