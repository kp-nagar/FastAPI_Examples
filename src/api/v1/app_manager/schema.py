from pydantic import BaseModel, Field, HttpUrl, EmailStr
from enum import Enum
from typing import Union # List python < 3.9 other use normal list.



class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserIn(UserOut):
    password: str


class Transfer(Enum):
    Credit = "in"
    Debit = "out"


class Image(BaseModel):
    url: HttpUrl
    name: str

    class Config:
        schema_extra = {
            "example": {
                "url": "https://www.example.com",
                "name": "Example"
            }
        }


class Item(BaseModel):
    name: str = Field(
        default="Item_1", title="The description of the item", max_length=10
    )   # handle in backend.
    description: Union[str, None] = None
    transfer: str = "in"
    price: float = Field(default=5, gt=0, description="The price must be greater than zero")
    tax: float
    tags: set[str] = set()
    category: list[str] = []
    images: Union[list[Image], None] = None


# When defining a Union, include the most specific type first, 
# followed by the less specific type. In the example below, 
# the more specific PlaneItem comes before CarItem in Union[PlaneItem, CarItem].

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None