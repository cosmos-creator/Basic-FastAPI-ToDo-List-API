# FastAPI To-Do List API

A REST API built with FastAPI that allows users to register, log in, and manage their own tasks. Each user can only view and manage tasks they created. Tasks are stored in a local SQLite database using SQLModel.

## Features

* User registration and login
* JWT-based authentication
* Per-user task isolation
* Add, view, update, and delete tasks
* SQLite storage via SQLModel
* Input validation using Pydantic
* HTTP error handling

## Installation

Clone the repository:

```bash
git clone https://github.com/cosmos-creator/Basic-FastAPI-ToDo-List-API.git
cd Basic-FastAPI-ToDo-List-API
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlmodel passlib[bcrypt] python-jose[cryptography] python-dotenv python-multipart
```

Set up your `.env` file:

```
SECRET_KEY=your_secret_key_here
```

## Running the API

```bash
uvicorn main:app --reload
```

Available at `http://127.0.0.1:8000` — interactive docs at `http://127.0.0.1:8000/docs`

## API Endpoints

### Auth

**POST /register** — Create a new account

```json
{
    "username": "cosmos-creator",
    "password": "yourpassword"
}
```

**POST /login** — Returns a JWT token (use the Authorize button in `/docs`)

### Tasks (require authentication)

**GET /** — Returns all tasks belonging to the logged-in user

**POST /add** — Add a new task

```json
{
    "name": "Finish project",
    "description": "Complete FastAPI To-Do API"
}
```

**PUT /update/{id}** — Update an existing task by ID

```json
{
    "name": "Updated task name",
    "description": "Updated description"
}
```

**DELETE /delete?id=1** — Delete a task by ID (only if it belongs to you)

## Authentication Flow

1. Register via `POST /register`
2. Log in via the **Authorize** button in `/docs`
3. All task routes are protected — requests without a valid token are rejected with 401

## Error Handling

| Status | Reason |
|--------|--------|
| 401 | Invalid credentials or missing/expired token |
| 403 | Attempting to modify another user's task |
| 404 | Task not found |
| 409 | Username already taken |

## Technologies Used

* Python
* FastAPI
* SQLModel
* SQLite
* JWT (python-jose)
* passlib (bcrypt)

## Purpose

Built as a learning project to practice:

* REST API development
* JWT authentication
* Database integration with SQLModel
* Dependency injection
* Per-user data isolation
