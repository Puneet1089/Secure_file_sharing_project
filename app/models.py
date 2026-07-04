# import req sqlalchemy column types
from sqlalchemy import Column, Integer, String, DateTime
# import base class
from app.database import Base


# file table model
class File(Base):
    __tablename__ ="files"   # db table name
    id=Column(Integer,primary_key=True,index=True)    # primary key
    file_id =Column(String(100), unique=True,nullable=False)   # unique link which is used in download link
    filename= Column(String(255), nullable=False)   # original file name which was uploaded
    filepath= Column(String(500), nullable=False)   # location of file on server
    uploaded_at = Column(DateTime,nullable=False)   # uploading timestamp
    expiry_time= Column(DateTime,nullable=False)   # link expiry time
    max_downloads =Column(Integer, nullable=False)  # max downloads allowed
    downloads_left =Column(Integer,nullable=False) # reemaining downloads
