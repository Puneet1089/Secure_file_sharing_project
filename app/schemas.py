# import basemodel from pydantic
from pydantic import BaseModel

# response format for upload api (structure)
class UploadResponse(BaseModel):
    message: str   # Success message
    file_id: str   # Unique file id
    download_link: str   # Download URL
