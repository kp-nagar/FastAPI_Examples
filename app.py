from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from util.logger import logger
from src.api.v1.app_manager.views import router

tags_metadata = [
    {
        "name": "Frontend Endpoints",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Backend Endpoints",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)


app.include_router(router, prefix="/api/v1", tags=["Backend Endpoints"])


@app.get("/", status_code=status.HTTP_200_OK, tags=["Frontend Endpoints"])
async def index_page():
    return "Flask Boilerplate Server is up."


@app.get("/lookup", status_code=status.HTTP_200_OK, tags=["Frontend Endpoints"])
async def lookup():
    from src.api.v1.app_manager.schema import Transfer
    return JSONResponse(
        # status_code=status.HTTP_201_CREATED,        # For custom status
        content={
            "transfer": [t.value for t in Transfer]
        }
    )
