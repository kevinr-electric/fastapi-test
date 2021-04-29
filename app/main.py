from enum import Enum
import json
from typing import Optional, List
import copy

from fastapi import FastAPI, Query, Path, HTTPException

from pydantic import BaseModel, Field
from pydantic.schema import schema

app = FastAPI()

class ItemType(str, Enum):
    """Food group of item"""
    meat="meat"
    vegetable="vegetable"
    fruit="fruit"
    dairy="dairy"
    other="other"


class Item(BaseModel):
    """
    A grocery item available for purchase
    """
    id: int = Field(..., description="ID of item")
    name: str = Field(..., description="name of item")
    type: ItemType = Field(..., description="type of item")
    price: Optional[float] = Field(0, description="dollar price of item")

class User(BaseModel):
    id: int = Field(..., description="ID of user")
    name: str = Field(..., description="name of user")
    items: List[Item] = Field([], description="list of Items the user has")

ITEMS = {
    1: Item(id=1, name="salmon", type=ItemType.meat, price=10.00),
    2: Item(id=2, name="bag", type=ItemType.other),
    3: Item(id=3, name="carrots", type=ItemType.vegetable, price=2.50),
    4: Item(id=4, name="pear", type=ItemType.fruit, price=3.29),
    5: Item(id=5, name="cheese", type=ItemType.dairy, price=8.20),
    6: Item(id=6, name="honeydew", type=ItemType.fruit, price=0.01)
}

USERS = {
    1: User(id=1, name="Bobby", items=[ITEMS[1], ITEMS[3], ITEMS[5], ITEMS[2]]),
    2: User(id=2, name="Billy", items=[ITEMS[4]])
}

@app.get("/healthcheck")
def healthcheck():
    return


@app.get("/items", response_model=List[Item])
def get_items(
    item_id: Optional[int] = Query(None, description="ID of the Item"),
    item_type: Optional[ItemType] = Query(None, description="Type of Items"),
) -> List[Item]:
    """Gets the items matching give query parameters"""
    if bool(item_id) == bool(item_type):
        raise HTTPException(status_code=400, detail="Exactly one of item_id and item_type must be specified")

    if item_id:
        return [ITEMS.get(item_id)]
    elif item_type:
        return [item for item in ITEMS.values() if item.type == item_type]
    else:
        None


@app.get("/user/{user_id}", response_model=User)
def get_user(
    user_id: int = Path(..., description="ID of the User"),
    item_type: Optional[ItemType] = Query(None, description="Type of Items"),
) -> User:
    """Gets the user specified"""
    user = copy.deepcopy(USERS.get(user_id))
    if item_type:
        user.items = [item for item in user.items if item.type == item_type]

    return user

# openapi_schema = app.openapi()
# openapi_schema = schema([Item, User], title='Pydantic Sample Schema')
# print(json.dumps(openapi_schema, indent=2))