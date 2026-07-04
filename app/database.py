# import function to create db connection
from sqlalchemy import create_engine
# import base class & session creator from sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
# import dotenv to read environment variables from .env file
from dotenv import load_dotenv
# import os module to access environment variables
import os

# load all variables from .env file
load_dotenv()

# creating db connection string using values from .env
DATABASE_URL = (
    f"mysql+mysqlconnector://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

# creating connection engine with mysql db
engine = create_engine(DATABASE_URL)

# creating a session factory for db operations
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# creating a base class that will be used by all db models
Base = declarative_base()

# creating a db session for every request
def get_db():
    db = SessionLocal()     # open db session
    try:
        yield db    # give session to api
    finally:
        db.close()   # always close db connection using finally
