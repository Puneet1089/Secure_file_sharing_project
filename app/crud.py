from sqlalchemy.orm import Session
from app.models import File


def save_file_record(db: Session, file):
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def get_file_record(db: Session, file_id: str):
    return db.query(File).filter(File.file_id == file_id).first()


def update_download_count(db: Session, file):
    if file.downloads_left > 0:
        file.downloads_left -= 1

    db.commit()
    db.refresh(file)

    return file

