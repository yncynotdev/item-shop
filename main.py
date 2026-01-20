from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, UploadFile
from sqlmodel import Session, Field, SQLModel, create_engine, select


class Items(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(index=True)
    types: str | None = Field(index=True)
    quantity: int | None = Field(default=None, index=True)
    img: str | None


db_file_name = "db/database.db"
db_url = f"sqlite:///{db_file_name}"

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


@app.on_event("startup")
def on_startup():
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
