# Basic FastAPI To-Do List API

A simple REST API built with FastAPI that allows users to create, view, and delete tasks. Tasks are stored in a local SQLite database using SQLModel, making it a lightweight project for learning API development, database integration, and error handling in Python.

## Features

* Add new tasks
* View all saved tasks
* Delete tasks by ID
* SQLite-based storage via SQLModel
* Input validation using Pydantic/SQLModel
* HTTP error handling for common edge cases

## Installation

Clone the repository:

```bash
git clone https://github.com/cosmos-creator/Basic-FastAPI-ToDo-List-API.git
cd Basic-FastAPI-ToDo-List-API
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlmodel
```

## Running the API

Start the server:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive documentation:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

### View Tasks

**GET /**

Returns all saved tasks.

### Add Task

**POST /add**

Example request body:

```json
{
    "name": "Finish project",
    "description": "Complete FastAPI To-Do API"
}
```

### Delete Task

**DELETE /delete?id=1**

Deletes the task with the given ID. Pass the ID as a query parameter.

## Data Storage

Tasks are stored in a local `database.sqlite` file, auto-created on startup.

Example task structure:

```json
{
    "id": 1,
    "name": "Finish project",
    "description": "Complete FastAPI To-Do API"
}
```

## Error Handling

The API handles several common cases:

* Empty task list
* Task not found on deletion
* Invalid query parameters

## Technologies Used

* Python
* FastAPI
* SQLModel
* SQLite

## Purpose

This project was built as a learning exercise to practice:

* REST API development
* Database integration with SQLModel
* Dependency injection
* Request validation
* HTTP status codes and error responses
