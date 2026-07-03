from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)

    file_id = Column(String(100), unique=True, nullable=False)

    filename = Column(String(255), nullable=False)

    filepath = Column(String(500), nullable=False)

    uploaded_at = Column(DateTime, nullable=False)

    expiry_time = Column(DateTime, nullable=False)

    max_downloads = Column(Integer, nullable=False)

    downloads_left = Column(Integer, nullable=False)