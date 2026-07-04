# import db engine & base clas
from app.database import Base, engine
# import file model such that sqlalchemy will know which table to create
from app.models import File

Base.metadata.create_all(bind=engine)    # creating all tables defined in models.py file
print("Database tables created successfully!")
