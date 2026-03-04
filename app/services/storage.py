import re

import boto3

from app.config import settings

_s3 = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

PRESIGNED_URL_EXPIRY = 3600


def _sanitize_name(name: str) -> str:
    return re.sub(r"[^\w\-.]", "_", name)


def generate_presigned_upload(
    filenames: list[str],
    content_types: list[str],
    category_name: str,
    user_id: str,
) -> list[dict[str, str]]:
    safe_category = _sanitize_name(category_name)
    results: list[dict[str, str]] = []

    for filename, content_type in zip(filenames, content_types):
        safe_filename = _sanitize_name(filename)
        key = f"{safe_category}/{user_id}/{safe_filename}"

        presigned_url = _s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.AWS_S3_BUCKET,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=PRESIGNED_URL_EXPIRY,
        )

        results.append(
            {
                "filename": filename,
                "presigned_url": presigned_url,
                "public_url": get_public_url(key),
                "key": key,
            }
        )

    return results


def get_public_url(key: str) -> str:
    return f"https://{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
