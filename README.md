# Basic FastAPI To-Do List API

A simple REST API built with FastAPI that allows users to create, view, and delete tasks. Tasks are stored in a local JSON file, making it a lightweight project for learning API development, file handling, and error handling in Python.

## Features

* Add new tasks
* View all saved tasks
* Delete tasks by ID
* JSON-based storage
* Input validation using Pydantic
* HTTP error handling for common edge cases

## Installation

Clone the repository:

```bash
git clone https://github.com/cosmos-creator/Basic-FastAPI-ToDo-List-API.git
cd Basic-FastAPI-ToDo-List-API
```

Install dependencies:

```bash
pip install fastapi uvicorn
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
    "description": "Complete FastAPI To-Do API",
    "key": 1
}
```

### Delete Task

**POST /done/**

Example request body:

```json
{
    "key": 1
}
```

## Data Storage

Tasks are stored in a local `tasks.json` file.

Example structure:

```json
{
    "1": {
        "Finish project": "Complete FastAPI To-Do API"
    }
}
```

## Error Handling

The API handles several common cases:

* Missing task file
* Duplicate task IDs
* Invalid task IDs
* Attempting to delete a task that does not exist
* Empty or unreadable task data

## Technologies Used

* Python
* FastAPI
* Pydantic
* JSON

## Purpose

This project was built as a learning exercise to practice:

* REST API development
* Request validation
* File operations
* JSON data handling
* HTTP status codes and error responses
