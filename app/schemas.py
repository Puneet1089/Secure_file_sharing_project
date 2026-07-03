from pydantic import BaseModel


class UploadResponse(BaseModel):
    message: str
    file_id: str
    download_link: str