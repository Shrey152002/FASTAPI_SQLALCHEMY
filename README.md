# FASTAPI_SQLALCHEMY
# Introduction to FastAPI and MySQL

FastAPI is a modern web framework for building APIs with Python, designed for speed and ease of use. MySQL is the world’s most popular relational database management system, widely used for web applications. This tutorial guides users through setting up a FastAPI application integrated with a MySQL database.

---

## Setting Up the Environment

1. **Create a Virtual Environment:**
   Use the following command to create a virtual environment, isolating dependencies for this project:
   ```bash
   python3 -m venv env
   ```

2. **Activate the Virtual Environment:**
   Activate the environment with:
   - **Linux/macOS:**
     ```bash
     source env/bin/activate
     ```
   - **Windows:**
     ```cmd
     .\env\Scripts\activate
     ```

3. **Install Dependencies:**
   Install the required packages using `pip`:
   ```bash
   pip install fastapi uvicorn sqlalchemy pymysql
   ```

---

## Creating the Database Connection

1. **Database Configuration:**
   - Create a `database.py` file to manage database connections.
   - Use SQLAlchemy to create an engine and define a session maker for efficient communication with the database.

2. **Database URL:**
   Configure the connection string to include authentication details and the database name, e.g.:
   ```python
   DATABASE_URL = "mysql+pymysql://username:password@localhost/db_name"
   ```

3. **Session Maker:**
   Define a session to handle database transactions:
   ```python
   from sqlalchemy.orm import sessionmaker
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   ```

---

## Defining Database Models

1. **User Model:**
   Create a `User` model to represent the `users` table:
   ```python
   from sqlalchemy import Column, Integer, String
   from database import Base

   class User(Base):
       __tablename__ = "users"
       id = Column(Integer, primary_key=True, index=True)
       username = Column(String, unique=True, index=True)
   ```

2. **Post Model:**
   Create a `Post` model to represent the `posts` table:
   ```python
   from sqlalchemy import Column, Integer, String, Text, ForeignKey
   from database import Base

   class Post(Base):
       __tablename__ = "posts"
       id = Column(Integer, primary_key=True, index=True)
       title = Column(String, index=True)
       content = Column(Text)
       user_id = Column(Integer, ForeignKey("users.id"))
   ```

---

## Building the FastAPI Application

1. **Main Application File:**
   - Create a `main.py` file to serve as the application’s entry point.
   - Instantiate FastAPI:
     ```python
     from fastapi import FastAPI
     app = FastAPI()
     ```

2. **Defining Routes:**
   - Create API endpoints for CRUD operations:
     - **Create User:** `POST /users`
     - **Retrieve Users:** `GET /users`
     - **Create Post:** `POST /posts`
     - **Delete Post:** `DELETE /posts/{id}`

3. **Example Endpoint:**
   ```python
   from fastapi import FastAPI, Depends
   from sqlalchemy.orm import Session
   from database import SessionLocal
   from models import User

   app = FastAPI()

   def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()

   @app.post("/users")
   async def create_user(user: User, db: Session = Depends(get_db)):
       db.add(user)
       db.commit()
       db.refresh(user)
       return user
   ```

---

## Deploying and Testing the API

1. **Running the Application:**
   Use Uvicorn to run the application:
   ```bash
   uvicorn main:app --reload
   ```
   The `--reload` flag enables hot-reloading during development.

2. **Testing Endpoints:**
   - Use tools like **Postman** or the **FastAPI interactive documentation** at `http://127.0.0.1:8000/docs`.
   - Test each API endpoint to confirm functionality.

3. **Validating Responses:**
   - Ensure successful requests return appropriate status codes (e.g., `200 OK`, `201 Created`).
   - Verify the integration between FastAPI and MySQL by checking the database entries.

---

By following these steps, you will have a fully functional FastAPI application integrated with a MySQL database, capable of handling CRUD operations efficiently.

