from typing import Annotated
from fastapi import (Depends, FastAPI, HTTPException,
                     UploadFile, File, Form, status)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from botocore.exceptions import ClientError
from database import SessionDep, get_session
from models.item import Item

import jwt
import logging
import seed
import config


app = FastAPI()


origins = [
    config.env.BETTER_AUTH_URL,
]


@app.on_event("startup")
def on_startup():
    get_session()
    seed.seed()


@app.get("/items")
def get_items(session: SessionDep,) -> list[Item]:
    item = session.exec(select(Item)).all()
    return item


@app.get("/items/{item_id}")
def get_item_by_id(item_id: int, session: SessionDep) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@app.get("/items/types/{types}")
def get_item_by_type(types: str, session: SessionDep) -> list[Item]:
    item = session.exec(select(Item).where(Item.types == types))
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@app.get("/items/name/{name}")
def get_item_by_name(name: str, session: SessionDep) -> list[Item]:
    item = session.exec(select(Item).where(Item.name == name))
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@app.post("/items/")
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
        config.s3.upload_file(
            temp_file_path, config.env.BUCKET_NAME, file.filename)
        image_url = f"{config.env.BUCKET_IMAGE_URL}/{file.filename}"
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


@app.post("/items/upload_image/")
async def insert_upload_image(file: UploadFile):
    if file.content_type not in 'image/png':
        raise HTTPException(status_code=400, detail="file unsupported format")

    temp_file_path = f"/tmp/{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        config.s3.upload_file(
            temp_file_path, config.env.BUCKET_NAME, file.filename)
    except ClientError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="can't upload files into cloud storage")

    return {"file_name": file.filename}


@app.delete("/items/{item_id}")
def delete_item_by_id(item_id: int, session: SessionDep) -> Item:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}


@app.get("/api/auth/verify")
def verify_auth(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    jwk_url = f"{config.env.BETTER_AUTH_URL}/{config.env.JWKS_URL}"

    token = credentials.credentials
    jwk = jwt.PyJWKClient(jwk_url)

    signing_key = jwk.get_signing_key_from_jwt(token).key

    try:
        payload = jwt.decode(
            jwt=token,
            key=signing_key,
            algorithms=[config.env.JWT_ALGORITHM],
            audience=[config.env.BETTER_AUTH_URL]
        )

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user id"
            )
        return {"user_id": user_id, "payload": payload}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        print(f"DEBUG JWT Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
