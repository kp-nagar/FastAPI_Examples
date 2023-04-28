from fastapi import APIRouter, status, Query, Path, Body, Form, File, UploadFile
from .schema import Item, Transfer, User, Image, UserIn, UserOut
from typing import Union, Annotated, Any
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/application_manager")


@router.get("/", status_code=status.HTTP_200_OK)
async def manager_page():
    return "This is application manager page."

@router.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user

@router.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


@router.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    print(dir(file))
    print(type(file))
    print(file)
    return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    print(dir(file))
    print(type(file))
    print(file)
    return {"filename": file.filename}

# Only Deprecate from GUI in postman it will work.
@router.get("/deprecate", summary="Example of Deprecate", status_code=status.HTTP_200_OK, deprecated=True)
async def manager_page():
    return "This is example of deprecate a path operation."

@router.post("/items/")
async def create_item(item: Item) -> Item:
    return item


@router.get("/items/")
async def read_items() -> list[Image]:
    return [
        Image(url="https://eee.vom", name="home"),
        Image(url="https://eee.vom", name="buy"),
    ]


@router.put("/items/other/", response_model=Item)
async def read_return_items(item: Item) -> Any:
    try:
        return item
    except Exception as e:
        print(e)


@router.post("/get_manager", response_model=Item,
             summary="Create an item",
            #  description="Create an item with all the information, name, description, price, tax and a set of unique tags", 
             response_description="The created item",
             status_code=status.HTTP_201_CREATED)
async def get_manager(item: Item):
    """
        Create an item with all the information:
        - **name**: each item must have a name
        - **description**: a long description
        - **price**: required
        - **tax**: if the item doesn't have tax, you can omit this
        - **tags**: a set of unique tag strings for this item
    """
    try:
        item.transfer = Transfer.Credit.name if item.transfer == Transfer.Credit.value else Transfer.Debit.value
    except Exception as e:
        print(e)
    else:
        return item
    
@router.post("/get_manager/body")
async def get_manager_body(item: Annotated[Item, Body(embed=True)]):
    """
        Create an item with all the information:
        - **name**: each item must have a name
        - **description**: a long description
        - **price**: required
        - **tax**: if the item doesn't have tax, you can omit this
        - **tags**: a set of unique tag strings for this item
    """
    try:
        item.transfer = Transfer.Credit.name if item.transfer == Transfer.Credit.value else Transfer.Debit.value
    except Exception as e:
        print(e)
    else:
        return item
    

@router.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


@router.post("/index-weights/") # key - int and value - float
async def create_index_weights(weights: dict[int, float]):
    print(weights)
    return weights


# Path Parameters
@router.get("/items/{item_id}")
# async def read_item(item_id: int):    This is Data validation example.
async def read_item(item_id: str, transfer_id: Annotated[Union[int, None], Query(gt=10)] = None, short: bool = False):
    item = {"item_id": item_id}
    if transfer_id:
        item.update({"transfer_id": transfer_id})
    if short:
        item.update({"short": short})
    return item


# Notice that, in this case, the item that would be taken from the body is optional. As it has a None default value.
@router.post("/create/item/{item_id}", status_code=status.HTTP_200_OK)
async def create_item(item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: Union[str, None] = None,
    item: Union[Item, None] = None,
):
    try:
        results = {"item_id": item_id}
        if q:
            results.update({"q": q})
        if item:
            results.update({"item": item})
        return results
    except Exception as exc:
        return JSONResponse(
            content={"error": exc.args[0]},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.put("/update/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

@router.put("/body/items/{item_id}")
async def update_body_item(item_id: int, item: Item, user: User, importance: Annotated[dict, Body()], goal: Annotated[int, Body(gt=0)],):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance, "Goal": goal}
    return results