# import os module for file and folder operations
import os
# import uuid module to generate unique id
import uuid

UPLOAD_FOLDER = "uploads"    # folder where uploaded files will be stored

# creating uploads folder if it not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# generating a unique id for every uploaded file
def generate_file_id():
    """
    Generate a unique ID for every uploaded file.
    """
    return str(uuid.uuid4())    # return random uuid as string

# saving uploaded file inside uploads folder
def save_uploaded_file(upload_file, file_id):
    """
    Save uploaded file inside uploads folder.
    """

    # get original file extension (like.pdf)
    extension = os.path.splitext(upload_file.filename)[1]

    # creating unique filename using uuid
    new_filename = f"{file_id}{extension}"

    # creating complete file path
    file_path = os.path.join(UPLOAD_FOLDER, new_filename)

    # saving uploaded file to my local storage
    with open(file_path, "wb") as file:
        file.write(upload_file.file.read())

    return file_path    # return saved file path
