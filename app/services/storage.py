import re

from fastapi import UploadFile
from supabase import create_client

from app.config import settings

_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


def _sanitize_name(name: str) -> str:
    return re.sub(r"[^\w\-.]", "_", name)


def upload_files(files: list[UploadFile], category_name: str, user_id: str) -> str:
    safe_category = _sanitize_name(category_name)
    bucket = settings.SUPABASE_STORAGE_BUCKET
    urls: list[str] = []

    for file in files:
        safe_filename = _sanitize_name(file.filename or "unnamed")
        path = f"{safe_category}/{user_id}/{safe_filename}"
        content = file.file.read()
        content_type = file.content_type or "application/octet-stream"

        _client.storage.from_(bucket).upload(
            path,
            content,
            file_options={"content-type": content_type},
        )

        public_url = _client.storage.from_(bucket).get_public_url(path)
        urls.append(public_url)

    return ",".join(urls)
