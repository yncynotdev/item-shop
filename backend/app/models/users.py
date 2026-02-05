from sqlmodel import SQLModel, Field


class Users(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    email: str | None = Field(index=True)
    name: str | None = Field(index=True)
