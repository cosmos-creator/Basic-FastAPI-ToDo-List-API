from fastapi import FastAPI, HTTPException
import os
import json
from pydantic import BaseModel, Field

app = FastAPI()

cwd = os.getcwd()
file = os.path.join(cwd, "tasks.json")

def check_file():
    # check whether file exists to even work with
    
    if not os.path.exists(file):
        raise HTTPException(status_code=404,detail="file tasks.json not found. Add New Task to initialize.")

@app.get("/")
def view_task():
    check_file()
    with open(file, 'r') as tasks:
        try:
            data = json.load(tasks)
        except Exception as e:
            raise HTTPException(status_code=200, detail="File was found but no tasks were there to show. Try adding new tasks.")
        
        return data

class Task(BaseModel):
    # PyDantic class for consistent data and data validation
    name: str
    description: str | None = None
    key: int = Field(gt=0) 
    # PyDantic helper used to add validation rules and metadata
    # gt: greater than

@app.post("/add")
def add_task(task: Task):
    # data = {
    #     task.key : { task.name : task.description }
    # }
    with open(file,"a+", encoding="utf-8") as tasks:
        tasks.seek(0)
        try:
            existing = json.load(tasks) # loads as a dict object
        except Exception as e:
            existing = {}

        tasks.truncate(0)
        if str(task.key) not in existing:
            existing[str(task.key)] = {task.name : task.description}
            json.dump(existing, tasks, indent=4,sort_keys=True)
        else:
            json.dump(existing, tasks, indent=4,sort_keys=True)
            raise HTTPException(status_code=409,detail="Task key already taken. Key must be unique and a positive integer.")
        

class TaskID(BaseModel):
    key: int

@app.post("/done/")
def delete_task(key: TaskID):
    check_file()
    with open(file,"a+", encoding="utf-8") as tasks:
        tasks.seek(0)
        try:
            existing = json.load(tasks) # loads as a dict object
        except Exception as e:
            existing = {}
        
        tasks.truncate(0) # deltes file content, everything, makes file size 0

        if str(key.key) in existing:
            del existing[str(key.key)]
            json.dump(existing, tasks, indent=4,sort_keys=True)
        else:
            json.dump(existing, tasks, indent=4,sort_keys=True)
            raise HTTPException(status_code=404, detail="Task not found.")