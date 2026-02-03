import app.services.item_service as item_service
from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Form
from app.db.database import SessionDep

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/items")
def get_items_handler(session: SessionDep,):
    return item_service.get_items(session)


@router.get("/items/{item_id}")
def get_item_by_id_handler(item_id: int, session: SessionDep):
    return item_service.get_item_by_id(item_id, session)


@router.get("/items/types/{types}")
def get_item_by_type_handler(types: str, session: SessionDep):
    return item_service.get_item_by_type(types, session)


@router.get("/items/name/{name}")
def get_item_by_name_handler(name: str, session: SessionDep):
    return item_service.get_item_by_name(name, session)


@router.post("/items/")
async def insert_item_handler(
        session: SessionDep,
        file: Annotated[UploadFile, File()],
        name: Annotated[str, Form()],
        types: Annotated[str, Form()],
        quantity: Annotated[int, Form()],
):
    items = await item_service.insert_item(
        session,
        file,
        name,
        types,
        quantity
    )

    return items


@router.post("/items/upload_image/")
async def insert_upload_image_handler(file: UploadFile):
    item_service.insert_upload_image(file)


@router.delete("/items/{item_id}")
def delete_item_by_id_handler(item_id: int, session: SessionDep):
    item_service.delete_item_by_id(item_id, session)
