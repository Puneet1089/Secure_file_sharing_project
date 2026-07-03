from datetime import datetime, timedelta

from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import File as FileModel
from app.schemas import UploadResponse
from app.utils import generate_file_id, save_uploaded_file
from app.crud import (
    save_file_record,
    get_file_record,
    update_download_count,
)

app = FastAPI(
    title="Secure File Sharing System",
    description="A backend application to upload files and share them securely using temporary download links.",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "message": "Secure File Sharing System is Running"
    }

@app.post("/upload", response_model=UploadResponse)
def upload_file(
    file: UploadFile = File(...),
    expiry_hours: int = Form(...),
    max_downloads: int = Form(...),
    db: Session = Depends(get_db)
):

    # Validation
    if expiry_hours <= 0:
        raise HTTPException(
            status_code=400,
            detail="Expiry hours must be greater than 0."
        )

    if max_downloads <= 0:
        raise HTTPException(
            status_code=400,
            detail="Max downloads must be greater than 0."
        )

    # Generate unique file id
    file_id = generate_file_id()

    # Save uploaded file
    file_path = save_uploaded_file(file, file_id)

    # Current time
    uploaded_at = datetime.now()

    # Calculate expiry
    expiry_time = uploaded_at + timedelta(hours=expiry_hours)

    # Create database object
    file_record = FileModel(
        file_id=file_id,
        filename=file.filename,
        filepath=file_path,
        uploaded_at=uploaded_at,
        expiry_time=expiry_time,
        max_downloads=max_downloads,
        downloads_left=max_downloads
    )

    # Save metadata
    save_file_record(db, file_record)

    return UploadResponse(
        message="File uploaded successfully.",
        file_id=file_id,
        download_link=f"http://127.0.0.1:8000/download/{file_id}"
    )

@app.get("/download/{file_id}")
def download_file(
    file_id: str,
    db: Session = Depends(get_db)
):

    # Get file from database
    file_record = get_file_record(db, file_id)

    # File not found
    if file_record is None:
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    # Check expiry
    if datetime.now() > file_record.expiry_time:
        raise HTTPException(
            status_code=403,
            detail="Download link has expired."
        )

    # Check download limit
    if file_record.downloads_left <= 0:
        raise HTTPException(
            status_code=403,
            detail="Download limit reached."
        )

    # Update remaining downloads
    update_download_count(db, file_record)

    # Return file
    return FileResponse(
        path=file_record.filepath,
        filename=file_record.filename
    )
