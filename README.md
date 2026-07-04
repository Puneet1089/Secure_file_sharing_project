# Secure File Sharing System

A backend application built using **Python, FastAPI, SQLAlchemy, and MySQL** that allows users to upload files and generate secure links.
Each uploaded file gets a unique link that automatically becomes invalid after a specified time or after a limited number of downloads.
The main goal of this project is to provide a simple and secure way to share files without keeping them publicly available forever.

---

# Features

- Upload files using FastAPI
- Generate unique download links using UUID
- Set expiry time for every uploaded file
- Limit the number of downloads
- Store file metadata in MySQL
- Automatic validation for invalid inputs
- Clean project structure using CRUD architecture
- Interactive Swagger API documentation

---

# Tech Stack

## Backend

- Python
- FastAPI

## Database

- MySQL

## ORM

- SQLAlchemy

## Server

- Uvicorn

## Other Libraries

- Python Dotenv
- Python Multipart
- UUID
- OS Module

---

# Project Structure

```
Secure_File_Sharing_Project/

│
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
│
├── uploads/
│
├── .env
├── init_db.py
├── requirements.txt
├── README.md
```

---

# How It Works

## Upload Flow

1. User uploads a file.
2. The system generates a unique UUID.
3. The file is saved inside the uploads folder.
4. File information is stored in MySQL.
5. A secure download link is returned.

---

## Download Flow

1. User opens the download link.
2. Backend checks whether the file exists.
3. Backend checks whether the link has expired.
4. Backend checks whether downloads are still available.
5. If everything is valid, the file is downloaded.

---

# Database Design

The project stores file metadata inside a MySQL table.

### Table: files

| Column | Description |
|----------|-------------|
| id | Primary Key |
| file_id | Unique UUID |
| filename | Original file name |
| filepath | File location |
| uploaded_at | Upload time |
| expiry_time | Link expiry time |
| max_downloads | Maximum allowed downloads |
| downloads_left | Remaining downloads |

---

# API Endpoints

## Home

```
GET /
```

Returns

```json
{
    "message": "Secure File Sharing System is Running"
}
```

---

## Upload File

```
POST /upload
```

Request

- File
- Expiry Hours
- Maximum Downloads

Response

```json
{
    "message": "File uploaded successfully.",
    "file_id": "generated_uuid",
    "download_link": "http://127.0.0.1:8000/download/generated_uuid"
}
```

---

## Download File

```
GET /download/{file_id}
```

Downloads the uploaded file after validating:

- File exists
- Link is not expired
- Download limit is available

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Secure-File-Sharing-System.git
```

Move into the project directory

```bash
cd Secure-File-Sharing-System
```

Install all required libraries

```bash
pip install -r requirements.txt
```

---

# Configure Environment Variables

Create a `.env` file in the project root.

Example

```env
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=3306
DB_NAME=secure_file_share
```

---

# Create Database

Open MySQL Workbench and execute

```sql
CREATE DATABASE secure_file_share;
```

---

# Create Tables

Run

```bash
python init_db.py
```

---

# Run the Project

```bash
uvicorn app.main:app --reload
```

---

# Swagger Documentation

After starting the server

Open

```
http://127.0.0.1:8000/docs
```

You can test all APIs directly from Swagger UI.

---

# Validation

The project validates

- Expiry hours must be greater than zero.
- Maximum downloads must be greater than zero.
- File must exist before downloading.
- Expired links are rejected.
- Download limit is checked before serving the file.

---

# Security Features

- UUID-based download links
- Download limit
- Link expiry validation
- File metadata stored in MySQL
- Environment variables stored using `.env`

---

# Future Improvements

Some features that can be added in future versions:

- User Authentication
- JWT Authorization
- AWS S3 Storage
- Docker Deployment
- Redis Caching
- Background Job for deleting expired files
- Email notifications
- Admin Dashboard
- File encryption
- Activity logs

---


# Author

**Puneet Bhardwaj**
Python Backend Developer
GitHub: https://github.com/Puneet1089
LinkedIn: https://www.linkedin.com/in/puneet-bhardwaj-3171482a3/
