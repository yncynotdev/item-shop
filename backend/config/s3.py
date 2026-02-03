import boto3
from config import (BUCKET_ENDPOINT_URL,
                    BUCKET_ACCESS_KEY_ID,
                    BUCKET_SECRET_ACCESS_KEY)


s3 = boto3.client(
    "s3",
    endpoint_url=BUCKET_ENDPOINT_URL,
    aws_access_key_id=BUCKET_ACCESS_KEY_ID,
    aws_secret_access_key=BUCKET_SECRET_ACCESS_KEY,
    region_name="auto",
)
