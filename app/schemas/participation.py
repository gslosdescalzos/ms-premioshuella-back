from datetime import datetime

from pydantic import BaseModel


class FilePresignRequest(BaseModel):
    filename: str
    content_type: str


class PresignUploadRequest(BaseModel):
    files: list[FilePresignRequest]


class PresignedFileInfo(BaseModel):
    filename: str
    presigned_url: str
    public_url: str
    key: str


class PresignUploadResponse(BaseModel):
    uploads: list[PresignedFileInfo]


class ParticipationResponse(BaseModel):
    id: int
    profile_id: str
    category_id: int
    content_url: str | None = None
    comments: str | None = None
    is_scout: bool | None = None
    scout_group: str | None = None
    phone: str | None = None
    participant_name: str | None = None
    participant_surname: str | None = None
    is_finalist: bool
    submitted_at: datetime

    model_config = {"from_attributes": True}
