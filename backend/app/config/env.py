import os
from dotenv import load_dotenv

load_dotenv()

BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL")

DB_PATH = os.getenv("DB_PATH")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWKS_URL = os.getenv("JWKS_URL")

BUCKET_NAME = os.getenv("BUCKET_NAME")
BUCKET_IMAGE_URL = os.getenv("BUCKET_IMAGE_URL")
BUCKET_ENDPOINT_URL = os.getenv("BUCKET_ENDPOINT_URL")
BUCKET_ACCESS_KEY_ID = os.getenv("BUCKET_ACCESS_KEY_ID")
BUCKET_SECRET_ACCESS_KEY = os.getenv("BUCKET_SECRET_ACCESS_KEY")
