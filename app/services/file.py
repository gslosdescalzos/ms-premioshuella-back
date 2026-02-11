import os
import re

from fastapi import UploadFile

from app.config import settings


def sanitize_name(name: str) -> str:
    return re.sub(r"[^\w\-.]", "_", name)


def save_files(
    files: list[UploadFile], category_name: str, username: str
) -> str:
    safe_category = sanitize_name(category_name)
    safe_username = sanitize_name(username)
    target_dir = os.path.join(settings.UPLOAD_DIR, safe_category, safe_username)
    os.makedirs(target_dir, exist_ok=True)

    for file in files:
        safe_filename = sanitize_name(file.filename or "unnamed")
        file_path = os.path.join(target_dir, safe_filename)
        with open(file_path, "wb") as f:
            content = file.file.read()
            f.write(content)

    return os.path.join(safe_category, safe_username)
