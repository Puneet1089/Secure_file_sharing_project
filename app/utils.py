import os
import uuid

UPLOAD_FOLDER = "uploads"

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def generate_file_id():
    """
    Generate a unique ID for every uploaded file.
    """
    return str(uuid.uuid4())


def save_uploaded_file(upload_file, file_id):
    """
    Save uploaded file inside uploads folder.
    """

    # Get file extension
    extension = os.path.splitext(upload_file.filename)[1]

    # Create unique filename
    new_filename = f"{file_id}{extension}"

    # Full file path
    file_path = os.path.join(UPLOAD_FOLDER, new_filename)

    # Save file
    with open(file_path, "wb") as file:
        file.write(upload_file.file.read())

    return file_path