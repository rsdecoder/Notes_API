# Notes_API

A secure Restful Notes API built with FastAPI, JWT Authentication and SQLAlchemy
Users can register, login and manage their own notes with full CRUD functionality.

### 🚀 Features:
* User registration and login
* Password hashing
* JWT-based authentication
* Protected endpoints
* User-owned resources (notes)
* Full CRUD for notes
* SQLite database
* clean project structure
* Environment variable configuration

### 🛠 Tech Stack
* Python
* FastAPI
* SQLite
* JWT (python-jose)
* Passlib
* Pydantic
* Uvicorn


### 📂 Project Structure
``` commandline
    app/
    |--- __init__.py
    |--- main.py
    |--- models.py
    |--- auth.py
    |--- crud.py
    |--- schemas.py
    |--- database.py
    |--- dependencies.py
    notes.db
    .env
    requirements.txt
    README.md

```

### ⚙️ Set up & Installation
1️⃣ Clone the repository 

    git clone https://github.com/rsdecoder/Notes_API.git
    cd Notes_API

2️⃣ Install dependencies

    pip install -r requirements.txt

3️⃣ Environment variables

Create a .env file in the project root: 

    SECRET_KEY = <your secret key here>
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

4️⃣ Run the application

    uvicorn app.main:app --reload

Server runs at:

    http://127.0.0.1:8000

### 🔐 Authentication Flow
1. Register a user
2. Login to receive a JWT access token
3. Send the token in the Authorization header for protected routes

    
    Authorization: Bearer <your_token_here>

#### 📌 API Endpoints
##### Auth

| Method | Endpoint     | Description                 |
|--------|--------------|-----------------------------|
| POST   | /register    | Register a new user         |
| POST   | /login       | Login and receive JWT token | 

##### Notes (Authenticated)

| Method | Endpoint       | Description          |
|--------|----------------|----------------------|
| POST   | /notes         | Create a note        |
| GET    | /notes         | Get user notes       | 
| PUT    | /notes/{id}    | Update a note        |
| DELETE | /notes/{id}    | Delete a note        | 


### 🔒 Security

* Passwords are hashed before storage
* JWT tokens are required for protected routes
* Users can only access and modify their own notes
