from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine
import config.env


connect_args = {"check_same_thread": False}
engine = create_engine(config.env.DB_PATH, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
