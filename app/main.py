# to get current date & time & calculating the expiry time
from datetime import datetime, timedelta

# to import fastapi
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException

# used for sending file back to the user for download
from fastapi.responses import FileResponse

# db session
from sqlalchemy.orm import Session

# import db dependency
from app.database import get_db

# import file model (changed the name beacuse of conflict with fastapi file)
from app.models import File as FileModel

# reesponse schema
from app.schemas import UploadResponse

# helper functions
from app.utils import generate_file_id, save_uploaded_file

# db operations
from app.crud import (
    save_file_record,
    get_file_record,
    update_download_count,
)

# creating fastapi application
app = FastAPI(
    title="Secure File Sharing System",
    description="An application to upload files and generate secure links.",
    version="1.0"
)

# home api

# simple api for checking whether server is running or not
@app.get("/")
def home():
    return {
        "message":"Secure File Sharing System is Running"
    }

# upload api

@app.post("/upload",response_model=UploadResponse)
def upload_file(
    # uploaded file
    file: UploadFile=File(...),

    # link expiry time (in hours)
    expiry_hours:int =Form(...),

    # max downloads allowed
    max_downloads: int= Form(...),

    # database session
    db:Session= Depends(get_db)
):
    # input validation

    # expiry time cannot be zero or negative
    if expiry_hours<= 0:
        raise HTTPException(
            status_code=400,
            detail="Expiry hours must be greater than 0."
        )
    
    # download limit cannot be zero or negative
    if max_downloads<=0:
        raise HTTPException(
            status_code=400,
            detail="Max downloads must be greater than 0."
        )

    # Generating unique link

    # Creating random UUID link 
    file_id =generate_file_id()
    # Save file in uploads folder
    file_path= save_uploaded_file(file, file_id)

    # Time Info

    # Current time upload
    uploaded_at=datetime.now()

    # calculating expiry time of the link
    expiry_time =uploaded_at+timedelta(hours=expiry_hours)

    # Creating Database Object

    # create 1 database record
    file_record = FileModel(
        file_id=file_id,
        filename=file.filename,
        filepath=file_path,
        uploaded_at=uploaded_at,
        expiry_time=expiry_time,
        max_downloads=max_downloads,
        downloads_left=max_downloads
    )

    # Saving metadata in Mysql

    save_file_record(db,file_record)

    # Return Response with the file id
    return UploadResponse(
        message="File uploaded successfully.",
        file_id = file_id,
        download_link= f"http://127.0.0.1:8000/download/{file_id}"
    )

# Download API
@app.get("/download/{file_id}")
def download_file(

    # receving the file_id from url
    file_id:str,
    # Database session
    db: Session= Depends(get_db)

):
    # Searching the file in database
    file_record =get_file_record(db, file_id)

    # if file doesnot exist
    if file_record is None:
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )
    # Checking download link is valid or not
    if datetime.now() >file_record.expiry_time:

        raise HTTPException(

            status_code=403,

            detail="Download link has expired."

        )
    # Checking the download limit
    if file_record.downloads_left<= 0:

        raise HTTPException(
            status_code=403,
            detail="Download limit reached."
        )
    # Reducing download count
    update_download_count(db, file_record)

    # Sending the file back to the user
    return FileResponse(
        path=file_record.filepath,
        filename=file_record.filename
    )
