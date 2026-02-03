from sqlmodel import SQLModel, Field


class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(index=True)
    types: str | None = Field(index=True)
    quantity: int | None = Field(default=None, index=True)
    image_url: str | None = Field(default=None)
