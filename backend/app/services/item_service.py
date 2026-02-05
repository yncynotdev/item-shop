import logging
from typing import Annotated
from fastapi import HTTPException, UploadFile, Form, File, status
from sqlmodel import select
from botocore.exceptions import ClientError
from app.db.database import SessionDep
from app.models.item import Item
from app.config.s3 import s3
from app.config.env import (
    BUCKET_IMAGE_URL,
    BUCKET_NAME,
)


def get_items(session: SessionDep,) -> list[Item]:
    item = session.exec(select(Item)).all()
    return item


def get_item_by_id(item_id: int, session: SessionDep) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item


def get_item_by_type(types: str, session: SessionDep) -> list[Item]:
    item = session.exec(select(Item).where(Item.types == types))
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item


def get_item_by_name(name: str, session: SessionDep) -> list[Item]:
    item = session.exec(select(Item).where(Item.name == name))
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item


async def insert_item(
        session: SessionDep,
        file: Annotated[UploadFile, File()],
        name: Annotated[str, Form()],
        types: Annotated[str, Form()],
        quantity: Annotated[int, Form()],
) -> Item:
    if file.content_type not in 'image/png':
        raise HTTPException(status_code=400, detail="file unsupported format")

    temp_file_path = f"/tmp/{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        s3.upload_file(
            temp_file_path, BUCKET_NAME, file.filename)
        image_url = f"{BUCKET_IMAGE_URL}/{file.filename}"
        session.add(Item(
            name=name,
            types=types,
            quantity=quantity,
            image_url=image_url
        ))
        session.commit()
    except ClientError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="can't upload files into cloud storage")

    return {"ok": True}


async def insert_upload_image(file: UploadFile):
    if file.content_type not in 'image/png':
        raise HTTPException(status_code=400, detail="file unsupported format")

    temp_file_path = f"/tmp/{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        s3.upload_file(
            temp_file_path, BUCKET_NAME, file.filename)
    except ClientError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="can't upload files into cloud storage")

    return {"file_name": file.filename}


def delete_item_by_id(item_id: int, session: SessionDep) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
