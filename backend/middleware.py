from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import BETTER_AUTH_URL


origins = [
    BETTER_AUTH_URL,
]


def cors_middleware(app: FastAPI):
    return app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
