# import session to perform db operations
from sqlalchemy.orm import Session
# import file model(files table)
from app.models import File

# saving a new file record into our db
def save_file_record(db: Session, file):
    db.add(file)   # add object in db session
    db.commit()   # save changes permanently
    db.refresh(file)   # refresh object to get latest value from db
    return file   # return saved object

# get file details using unique file_id
def get_file_record(db: Session, file_id: str):
    return db.query(File).filter(File.file_id ==file_id).first()   # search the files table and return first matching record

# reduce remaining download count
def update_download_count(db: Session, file):
    if file.downloads_left > 0:   #  if downloads are avialble then decerease
        file.downloads_left-=1

    db.commit()   # save updated value
    db.refresh(file)   # refresh object with latest db values
    return file
