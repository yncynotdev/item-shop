from fastapi import FastAPI

from app.seed import seed
from app.config.env import BETTER_AUTH_URL
from app.db.database import get_session
from app.routers import item
from app.internal import auth


app = FastAPI()


origins = [
    BETTER_AUTH_URL,
]


@app.on_event("startup")
def on_startup():
    get_session()
    seed()


app.include_router(item.router)
app.include_router(auth.router)
