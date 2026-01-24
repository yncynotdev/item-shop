from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, Field, SQLModel, create_engine, select
from dotenv import load_dotenv

import jwt
import os


BASE_URL = os.getenv("BETTER_AUTH_URL")
BASE_HTTP_URL = os.getenv("BETTER_AUTH_HTTP_URL")
DB_PATH = os.getenv("DB_PATH")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWKS_URL = os.getenv("JWKS_URL")

load_dotenv()


class Items(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(index=True)
    types: str | None = Field(index=True)
    quantity: int | None = Field(default=None, index=True)
    img: str | None


class Users(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    email: str | None = Field(index=True)
    name: str | None = Field(index=True)


def check_env():
    if BASE_URL is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="BASE_URL is missing"
        )

    if BASE_HTTP_URL is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="BASE_HTTP_URL is missing"
        )

    if JWT_ALGORITHM is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT_ALGORITHM is missing"
        )

    if JWKS_URL is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWKS_URL is missing"
        )

    if DB_PATH is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="DB_PATH is missing"
        )


db_url = f"sqlite:///{DB_PATH}"

connect_args = {"check_same_thread": False}
engine = create_engine(db_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def seed():
    with Session(engine) as session:
        exists = session.exec(select(Items)).first()
        if exists:
            return

        items = [
            Items(name="Broad Sword", types="Weapon", quantity=1, img=""),
            Items(name="Bronze Helmet", types="Weapon", quantity=1, img=""),
            Items(name="Bronze Armor", types="Armor", quantity=1, img=""),
            Items(name="Healing Potion(S)",
                  types="Consumables", quantity=5, img=""),
            Items(name="Mana Potion(S)", types="Consumables", quantity=5, img=""),
        ]

        session.add_all(items)
        session.commit()


app = FastAPI()


origins = [
    BASE_URL,
    BASE_HTTP_URL
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def on_startup():
    check_env()
    seed()


@app.get("/items")
def get_items(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100
) -> list[Items]:
    item = session.exec(select(Items).offset(offset).limit(limit)).all()
    return item


@app.get("/items/{item_id}")
def get_item_by_id(item_id: int, session: SessionDep) -> Items:
    item = session.get(Items, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@app.get("/items/types/{types}")
def get_item_by_type(types: str, session: SessionDep) -> list[Items]:
    item = session.exec(select(Items).where(Items.types == types))
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@app.get("/items/name/{name}")
def get_item_by_name(name: str, session: SessionDep) -> list[Items]:
    item = session.exec(select(Items).where(Items.name == name))
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@app.post("/items/")
def insert_item(items: Items, session: SessionDep, file: UploadFile) -> Items:
    session.add(items)
    session.commit()
    session.refresh(items)
    return items


@app.post("/items/upload_file/")
async def insert_upload_image(file: UploadFile):
    if file.content_type not in 'image/png':
        raise HTTPException(status_code=400, detail="file unsupported format")

    return {"file_name": file.filename}


@app.delete("/items/{item_id}")
def delete_item_by_id(item_id: int, session: SessionDep) -> Items:
    item = session.get(Items, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}


@app.get("/api/auth/verify")
def verify_auth(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    jwk_url = f"{BASE_URL}/{JWKS_URL}"

    token = credentials.credentials
    jwk = jwt.PyJWKClient(jwk_url)

    signing_key = jwk.get_signing_key_from_jwt(token).key

    try:
        payload = jwt.decode(
            jwt=token,
            key=signing_key,
            algorithms=["EdDSA"],
            audience=["http://localhost:3000", "http://127.0.0.1:3000"]
            # options={"verify_aud": False}
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
            detail=f"Internal server error: {str(e)}"
        )
